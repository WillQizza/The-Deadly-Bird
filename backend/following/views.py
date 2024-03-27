from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers
from .models import Following, FollowingRequest
from .serializers import FollowRequestSerializer, FollowingSerializer
from identity.models import Author, InboxMessage
from deadlybird.permissions import RemoteOrSessionAuthenticated, SessionAuthenticated, IsGetRequest, IsPutRequest, IsPostRequest, IsDeleteRequest
from deadlybird.pagination import Pagination, generate_pagination_query_schema
from deadlybird.serializers import GenericErrorSerializer, GenericSuccessSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from deadlybird.settings import SITE_HOST_URL
from nodes.util import get_auth_from_host
from deadlybird.util import resolve_remote_route, compare_domains
from identity.util import check_author_is_remote
from identity.serializers import AuthorSerializer
import requests
import json


@extend_schema(
    parameters=[
        OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id to check for following"),
        OpenApiParameter("target_author_ids", type=str, location=OpenApiParameter.QUERY, description="Reduced subset of author ids to search from"),
        *generate_pagination_query_schema()
    ],
    responses=FollowingSerializer
)
@api_view(["GET"])
@permission_classes([RemoteOrSessionAuthenticated])
def following(request, author_id: str):
    """
    URL: ://service/authors/{AUTHOR_ID}/following
    GET [local, remote]: get a list of authors who AUTHOR_ID is following 
    query parameters:
        - target_author_ids: string[], a reduced subset of author_id's to search from.
    """
    # Get target author ids if target_author_ids parameter is present
    include_author_ids = []
    include_author_ids_str = request.query_params.get('include_author_ids', None)
    if include_author_ids_str:
        include_author_ids = list(map(int, include_author_ids_str.split(',')))

    # Search a subset of author ids if target_author_ids parameter is present
    if include_author_ids: 
        following = Following.objects.filter(
            target_author_id__in=include_author_ids, author_id=author_id
        ).select_related('author')\
         .order_by('id')
    # Otherwise search author ids
    else:
        following = Following.objects.filter(target_author_id=author_id)\
            .select_related('author')\
            .order_by('id')

    # Return serialized results
    serializer = FollowingSerializer([f.author for f in following])
    return Response(serializer.data)

@extend_schema(
    operation_id="api_authors_followers_retrieve_all",
    parameters=[
        OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id to check for followers"),
        *generate_pagination_query_schema()
    ],
    responses=FollowingSerializer
)
@api_view(["GET"])
@permission_classes([RemoteOrSessionAuthenticated])
def followers(request, author_id: str):
    """
    URL: ://service/authors/{AUTHOR_ID}/followers
    GET [local, remote]: get a list of authors who are AUTHOR_ID's followers       
    """
    # Get authors who are following author id
    followers = [f.author for f in Following.objects.filter(target_author_id=author_id)\
        .select_related('author')\
        .order_by('id')]
    
    # Return serialized results
    return Response(FollowingSerializer(followers).data)

@extend_schema(
    parameters=[
        OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id to interact with"),
        OpenApiParameter("foreign_author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Foreign author id to interact with in relation to author id"),
    ]
)
@extend_schema(
    methods=["GET"],
    responses={
        400: GenericErrorSerializer,
        404: GenericErrorSerializer,
        200: FollowingSerializer
    }
)
@extend_schema(
    methods=["DELETE"],
    responses={
        400: GenericErrorSerializer,
        404: GenericErrorSerializer,
        204: GenericSuccessSerializer
    }
)
@extend_schema(
    methods=["PUT"],
    request=None,
    responses={
        400: GenericErrorSerializer,
        409: GenericErrorSerializer,
        201: GenericSuccessSerializer
    }
)

@api_view(['DELETE', 'PUT', 'GET'])
@permission_classes([(IsGetRequest & RemoteOrSessionAuthenticated) | ((IsDeleteRequest | IsPutRequest) & SessionAuthenticated)])
def modify_follower(request, author_id: str, foreign_author_id: str): 
    """ 
    URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    DELETE [local]: remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
    PUT [local]: Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
    GET [local, remote] check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
    """

    # The foreign author id are meant to be an url encoded URL of the foreign author. So in the case scenario we receive a url encoded author, parse and extract last id.
    if foreign_author_id.startswith("http://") or foreign_author_id.startswith("https://"):
        foreign_author_id = foreign_author_id.split("/")[-1]

    # Check that request is not to self
    if author_id == foreign_author_id:
        return Response({
            "error": True,
            "message": "Can not request to self"
        }, status=400)

    foreign_author = Author.objects.filter(id=foreign_author_id).first()
    author = Author.objects.filter(id=author_id).first()
    
    if not foreign_author or not author:
        return Response({
            "error": True,
            "message": "Can not identify one or both provided authors"
        }, status=404)
   
    if request.method == "DELETE":
        obj = get_object_or_404(Following, author_id=foreign_author_id, target_author_id=author_id)
        obj.delete()
        # if author we are following is remote, then send unfollow request
        if check_author_is_remote(author_id):
            remote_route = resolve_remote_route(author.host, view="inbox", kwargs={
                "author_id": author_id,
            })
            auth = get_auth_from_host(author.host)
            post_json = {
                "type": "Unfollow",
                "summary": f"{foreign_author.display_name} wants to unfollow {author.display_name}",
                "actor": AuthorSerializer(foreign_author).data,
                "object": AuthorSerializer(author).data,
            }
            requests.post(
                url=remote_route, 
                headers={'Content-Type': 'application/json'},
                data=json.dumps(post_json),
                auth=auth,
            )
        return Response({"error": False, "message": "Follower removed successfully."}, status=204)

    elif request.method == "PUT": 
        Following.objects.get_or_create(
            author_id=foreign_author_id,
            target_author_id=author_id
        )
        follow_req = FollowingRequest.objects.filter(
            author_id=foreign_author_id, 
            target_author_id=author_id
        ).first()

        if follow_req:
            inbox_msg = InboxMessage.objects.filter(content_id=follow_req.id).first()
            if inbox_msg:
                inbox_msg.delete()
            follow_req.delete()

        # send follow response (can be remote or local)
        if not compare_domains(foreign_author.host, SITE_HOST_URL):
            route = resolve_remote_route(foreign_author.host, view="inbox", kwargs={
                "author_id": foreign_author_id,
            })
            auth = get_auth_from_host(foreign_author.host)
            post_json = {
                "type": "FollowResponse",
                "summary": f"{author.display_name} accepted your follow request",
                "actor": AuthorSerializer(author).data,
                "object": AuthorSerializer(foreign_author).data,
                "accepted": True,
            }
            requests.post(
                url=route,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(post_json),
                auth=auth,
            )

        return Response({"error": False, "message": "Follower added successfully."}, status=201)
    
    elif request.method == 'GET':

        if not compare_domains(SITE_HOST_URL, author.host):
            # send to remote author
            remote_route = resolve_remote_route(author.host, view="modify_follower", args=[author_id, foreign_author_id])
            
            auth = get_auth_from_host(author.host)
            response = requests.get(url=remote_route, auth=auth) 

            if response.status_code == 200:
                # synrchonize with remote
                existing_request = FollowingRequest.objects.filter(
                    author_id=foreign_author_id, target_author_id=author_id
                ).first()
                if existing_request:
                    Following.objects.get_or_create(
                        author_id=foreign_author_id,
                        target_author_id=author_id
                    )
                    existing_request.delete()
                    return Response(response.json())
                else:
                    existing_follow = Following.objects.filter(
                        author_id=foreign_author_id,
                        target_author_id=author_id
                    ).first()
                    if existing_follow is not None:
                        # already replicated
                        return Response(response.json())
                    else:
                        return Response({"message": "prerequisite follow request object missing."}, status=404)
            elif response.status_code == 404:
                existing_follow = Following.objects.filter(
                    author_id=foreign_author_id, target_author_id=author_id
                ).first()
                if existing_follow:
                    # synchronize with remote
                    existing_follow.delete()
                return Response({"error": True, "message": "Not following relationship found"}, status=404)
            else:
                return Response({"error": True, 
                                 "message": f"Remote node failed with status {response.status_code}"
                                }, status=response.status_code)
        else:
            follow = Following.objects.filter(
                author_id=foreign_author_id, target_author_id=author_id
            ).first()

            if follow is not None:
                serializer = FollowingSerializer(follow)
                return Response(serializer.data)
            else:
                return Response({"message": "No follow object found."}, status=404)
 
@extend_schema(
    parameters=[
        OpenApiParameter("local_author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id to interact with"),
        OpenApiParameter("foreign_author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Foreign author id to interact with in relation to author id")
    ]
)
@extend_schema(
    methods=["POST"],
    request=None,
    responses={
        400: GenericErrorSerializer,
        403: GenericErrorSerializer,
        404: GenericErrorSerializer,
        409: GenericErrorSerializer,
        201: GenericSuccessSerializer,
        500: GenericErrorSerializer
    }
)
@extend_schema(
    methods=["GET"],
    responses={
        404: GenericErrorSerializer,
        200: FollowRequestSerializer
    }
)
@api_view(["GET", "DELETE"])
@permission_classes([RemoteOrSessionAuthenticated])
def request_follower(request: HttpRequest, author_id: str, target_author_id: str):
    """
    Request a follower on local or foreign host.
    URL: None specified
    """
    if request.method == "GET":
        follow_req = FollowingRequest.objects.filter(
            author_id=author_id, target_author_id=target_author_id
        ).first()

        if follow_req is not None:
            serializer = FollowRequestSerializer(follow_req)
            return Response(serializer.data)
        else:
            return Response({"message": "Follow Request not found", "status": 404}, status=404) 
    elif request.method == "DELETE":
        author = Author.objects.filter(id=author_id).first()
        target_author = Author.objects.filter(id=target_author_id).first()
        if not target_author or not author:
            return Response({
                "error": True,
                "message": "Can not indentify one or both provided authors"
            }, status=404)

        follow_req = FollowingRequest.objects.filter(
            author_id=author_id, target_author_id=target_author_id
        ).first()

        if follow_req:
            # delete inbox message
            inbox_msg = InboxMessage.objects.filter(content_id=follow_req.id).first()
            if inbox_msg:
                inbox_msg.delete()

            # delete follow request
            follow_req.delete()

        # send follow response (can be remote or local)
        if check_author_is_remote(author_id):
            route = resolve_remote_route(author.host, view="inbox", kwargs={
                "author_id": author_id,
            })
            auth = get_auth_from_host(author.host)
            post_json = {
                "type": "FollowResponse",
                "summary": f"{target_author.display_name} rejected your follow request",
                "actor": AuthorSerializer(target_author).data,
                "object": AuthorSerializer(author).data,
                "accepted": False,
            }
            requests.post(
                url=route,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(post_json),
                auth=auth,
            )

        return Response({
            "message": "Successfully deleted follow request"
        }, status=204)
