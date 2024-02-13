#TODO: figure out CSRF stuff

from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from identity.util import check_authors_exist, validate_login_session
from .models import Following, FollowingRequest
from .serializers import FollowingSerializer
from identity.models import Author
from django.views.decorators.csrf import csrf_exempt
from deadlybird.pagination import Pagination

@api_view(["GET"])
def followers(request, author_id:int):

    """
    URL: ://service/authors/{AUTHOR_ID}/followers
    GET [local, remote]: get a list of authors who are AUTHOR_ID's followers    
    """
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


@api_view(['DELETE', 'PUT', 'GET'])
def modify_follower(request, author_id, foreign_author_id):
    
    """ 
    URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    DELETE [local]: remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
    PUT [local]: Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
    GET [local, remote] check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
    """

    # TODO: determine if authentication for PUT but not for others is right
    if request.method == 'PUT':
        session_valid = validate_login_session(request)
        if not session_valid:
            return Response({"message": "Authentication required"}, status=403)
    
    try:
        if request.method == 'DELETE':
            obj = get_object_or_404(Following, author_id=foreign_author_id, target_author_id=author_id)
            obj.delete()
            return Response({"message": "Follower removed successfully."}, status=204)

        elif request.method == 'PUT':
            _, created = Following.objects.get_or_create(
                author_id=foreign_author_id,
                target_author_id=author_id
            )
            if created:
                return Response({"message": "Follower added successfully."}, status=201)
            else:
                return Response({"message": "The follower already exists."}, status=200)

        elif request.method == 'GET':
            obj = get_object_or_404(Following, author_id=foreign_author_id, target_author_id=author_id)
            serializer = FollowingSerializer(obj)
            return Response(serializer.data)

    except Following.DoesNotExist:
        if request.method == 'GET':
            return Response({"message": "Follower does not exist."}, status=404)
        return Response({"message": "Unexpected error occurred."}, status=400)
    

@api_view(["POST"])
def request_follower(request, local_author_id:int, foreign_author_id:int):
    """
    Request a follower on local or foreign host.
    URL: None specified
    """

    session_valid = validate_login_session(request)
    if not session_valid:
        return Response({"message": "Authentication required"}, status=403)

    if not check_authors_exist(local_author_id, foreign_author_id):
        return Response({
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
                "message": "Conflict: Outstanding request in existence"
            }, status=409)

    if local_author.host != foreign_author.host:
        # TODO: handle remote host inbox object: 
        # https://uofa-cmput404.github.io/general/project.html#friendfollow-request
        return Response({
            "error": True,
            "message": "remote inboxed not supported yet"
        })
    else:
        FollowingRequest.objects.create(
            target_author_id = foreign_author_id,
            author_id = local_author_id
        )

        # TODO: notfiy inbox 

        return Response({
            "error": False,
            "message": "Follow Request Created"
        }, status=201)