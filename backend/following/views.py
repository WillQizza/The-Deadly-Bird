#TODO: figure out CSRF stuff

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from identity.util import check_authors_exist, validate_login_session
from .models import Following, FollowingRequest
from identity.models import Author
from django.views.decorators.csrf import csrf_exempt

@api_view(["POST"])
@csrf_exempt
def follow(request, target_author_id:int): 

    session_valid = validate_login_session(request)
    if isinstance(session_valid, Response):
        return session_valid

    author_id = request.session["id"]
    
    if not check_authors_exist(author_id, target_author_id):
        return Response({
            "message": "Author does not exist"
        }, status=404)

    if Following.objects.filter(author__id=author_id, target_author__id=target_author_id).exists(): 
        return Response({
            "message": "Conflict: Author is already following"
        }, status=409)

    if FollowingRequest.objects.filter(author__id=author_id, 
        target_author__id=target_author_id).exists():
            return Response({
                "message": "Conflict: Outstanding request in existence"
            }, status=409)

    FollowingRequest.objects.create(
        author_id=author_id, target_author_id=target_author_id
    )

    return Response({"message": "Created: Follow Request"}, status=201)

@api_view(["POST"])
@csrf_exempt
def accept_follow(request, follow_req_id:int):
    
    session_valid = validate_login_session(request)
    if isinstance(session_valid, Response):
        return session_valid
    
    author_id = request.session["id"]
    if not check_authors_exist(author_id):
        return Response({
            "message": "Author does not exist"
        }, status=404) 
    
    if not FollowingRequest.objects.filter(id=follow_req_id).exists(): 
            return Response({
                "message": "Not Available: No pending follow request"
            }, status=409)

    try:
        follow_request = FollowingRequest.objects.get(id=follow_req_id, target_author_id=author_id)
        Following.objects.create(
            author_id=follow_request.author_id,
            target_author_id=author_id
        )
        follow_request.delete()
        return Response({"message": "Follow Accepted"}, status=201)
    
    except Exception as e:
        return Response({"message": f"Internal Server Error: Follow could not be accepted {e}"}, status=500)
         

@api_view(["POST"])
@csrf_exempt
def unfollow(request, target_author_id:int):
 
    session_valid = validate_login_session(request)
    if isinstance(session_valid, Response):
        return session_valid
    
    author_id = request.session["id"]
    
    if not check_authors_exist(author_id, target_author_id):
        return Response({
            "message": "Author does not exist"
        }, status=404) 
    
    if not Following.objects.filter(author__id=author_id, target_author__id=target_author_id).exists(): 
        return Response({
            "message": "Not Available: Author is not following"
        }, status=409)

    Following.objects.delete(
        author_id=author_id, target_author_id=target_author_id
    )

    return Response({"message": "Created: Follow Request"}, status=201)