from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from identity.util import check_authors_exist, validate_login_session
from .models import Following, FollowingRequest
from .serializers import FollowRequestSerializer, FollowingSerializer
from identity.models import Author, InboxMessage
from deadlybird.pagination import Pagination


@api_view(["GET"])
def following(request, author_id: str):
    """
    URL: ://service/authors/{AUTHOR_ID}/following
    GET [local, remote]: get a list of authors who AUTHOR_ID is following
    
    query parameters:
        - target_author_ids: string[], a reduced subset of author_id's to search from.
    """

    include_author_ids = []
    include_author_ids_str = request.query_params.get('include_author_ids', None)
    if include_author_ids_str:
        include_author_ids = list(map(int, include_author_ids_str.split(',')))

    if include_author_ids: 
        queryset = Following.objects.filter(
            target_author_id__in=include_author_ids, author_id=author_id
        ).select_related('author')\
         .order_by('id')
    else:
        queryset = Following.objects.filter(target_author_id=author_id)\
            .select_related('author')\
            .order_by('id')

    paginator = Pagination()
    page = paginator.paginate_queryset(queryset, request)

    if page is not None:
        authors = [following.author for following in page]
        serializer = FollowingSerializer(authors)
        return paginator.get_paginated_response(serializer.data)
    else:
        authors = [following.author for following in queryset]
        serializer = FollowingSerializer(authors)
        return Response(serializer.data)

@api_view(["GET"])
def followers(request, author_id: str):

    """
    URL: ://service/authors/{AUTHOR_ID}/followers
    GET [local, remote]: get a list of authors who are AUTHOR_ID's followers       
    """
    queryset = Following.objects.filter(target_author_id=author_id)\
        .select_related('author')\
        .order_by('id')

    paginator = Pagination("followers")
    page = paginator.paginate_queryset(queryset, request)
    
    if page is not None:
        authors = [following.author for following in page]
        serializer = FollowingSerializer(authors)
        return paginator.get_paginated_response(serializer.data)
    else:
        authors = [following.author for following in queryset]
        serializer = FollowingSerializer(authors)
        return Response(serializer.data)  

@api_view(['DELETE', 'PUT', 'GET'])
def modify_follower(request, author_id, foreign_author_id):
    
    """ 
    URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    DELETE [local]: remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
    PUT [local]: Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
    GET [local, remote] check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
    """
    if author_id == foreign_author_id:
        return Response({
            "error": True,
            "message": "Can not request to self"
            }, status=400)

    # TODO: determine if authentication for PUT but not for others is right
    if request.method == 'PUT':
        session_valid = validate_login_session(request)
        if not session_valid:
            return Response({"message": "Authentication required"}, status=403)
    
    try:
        if request.method == 'DELETE':
            obj = get_object_or_404(Following, author_id=foreign_author_id, target_author_id=author_id)
            obj.delete()
            return Response({"error": False, "message": "Follower removed successfully."}, status=204)

        elif request.method == 'PUT':
            try: 
                Following.objects.get_or_create(
                    author_id=foreign_author_id,
                    target_author_id=author_id
                )
                try:
                    follow_req = FollowingRequest.objects.filter(
                        author_id=foreign_author_id, 
                        target_author_id=author_id
                    ).first()

                    InboxMessage.objects.filter(content_id=follow_req.id).delete()
                    follow_req.delete() #delete after inbox message because of dependancy
                    return Response({"message": "Follower added successfully."}, status=201)
                except:
                    return Response({"message": "Follower already added."}, status=201) 
            except: 
                return Response({"message": "Failed to create follower."}, status=200)

        elif request.method == 'GET':
            obj = get_object_or_404(Following, author_id=foreign_author_id, target_author_id=author_id)
            serializer = FollowingSerializer(obj)
            return Response(serializer.data)

    except Following.DoesNotExist:
        if request.method == 'GET':
            return Response({"message": "Follower does not exist."}, status=404)
        return Response({"message": "Unexpected error occurred."}, status=400)
    

@api_view(["POST", "GET"])
def request_follower(request: HttpRequest, local_author_id: str, foreign_author_id: str):
    """
    Request a follower on local or foreign host.
    URL: None specified
    """
    
    if request.method == "GET":
        follow_req = FollowingRequest.objects.filter(
            author=local_author_id,
            target_author=foreign_author_id
        ).first()

        follow_req = get_object_or_404(FollowingRequest, 
                                       author_id=local_author_id, 
                                       target_author_id=foreign_author_id)
        serializer = FollowRequestSerializer(follow_req)
        return Response(serializer.data)
         
    elif request.method == "POST":
        session_valid = validate_login_session(request)
        if not session_valid:
            return Response({
                "error": True,
                "message": "Authentication required"
            }, status=403)

        if not check_authors_exist(local_author_id, foreign_author_id):
            return Response({
                "error": True,
                "message": "An author provided does not exist"
            }, status=404) 

        local_author = Author.objects.get(id=local_author_id)
        foreign_author = Author.objects.get(id=foreign_author_id)
        
        if Following.objects.filter(author__id=local_author_id,
                                    target_author__id=foreign_author_id).exists(): 
            return Response({
                "message": "Conflict: Author is already following"
            }, status=409)

        elif FollowingRequest.objects.filter(author__id=local_author_id, 
            target_author__id=foreign_author_id).exists():
                return Response({
                    "error": True,
                    "message": "Conflict: Outstanding request in existence"
                }, status=409)

        if local_author.host != foreign_author.host:
            # TODO: handle remote host inbox object: 
            # https://uofa-cmput404.github.io/general/project.html#friendfollow-request
            return Response({
                "error": True,
                "message": "remote inboxed not supported yet"
            }, status=400)
        else:
            try:
                follow_req = FollowingRequest.objects.create(
                    target_author_id=foreign_author_id,
                    author_id=local_author_id
                )

                InboxMessage.objects.create(
                    author_id=foreign_author_id,
                    content_id=follow_req.id,
                    content_type=InboxMessage.ContentType.FOLLOW
                )

                return Response({
                    "error": False,
                    "message": "Follow Request Created"
                }, status=201)          

            except Exception:
                return Response({
                    "error": True,
                    "message": "Failed to create FollowRequest or InboxMessage"
                }, status=500)