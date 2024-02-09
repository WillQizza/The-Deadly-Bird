#TODO: figure out CSRF stuff

from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from identity.util import check_authors_exist, validate_login_session
from .models import Following, FollowingRequest
from .serializers import FollowingSerializer
from identity.models import Author
from django.views.decorators.csrf import csrf_exempt
from deadlybird.pagination import CustomPagination

@api_view(["GET"])
def followers(request, author_id:int):

    """
    URL: ://service/authors/{AUTHOR_ID}/followers
    GET [local, remote]: get a list of authors who are AUTHOR_ID's followers    
    """

    queryset = Following.objects.filter(target_author_id=author_id)\
        .select_related('author')\
        .order_by('id')

    paginator = CustomPagination()

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
    Note: No URL format specified on the spec. I think this is because the only foreign host interfaces through sending
    messages in the foreign authors inbox, so this view is like a private view for our server -- no foreign host needs this
    route. 
    """
    if request.method == "POST":

        session_valid = validate_login_session(request)
        if not session_valid:
            return Response({"message": "Authentication required"}, status=403)

        if not check_authors_exist(local_author_id, foreign_author_id):
            return Response({
                "message": "An author provided does not exist"
            }, status=404) 

        local_author = Author.objects.get(id=local_author_id)
        foreign_author = Author.objects.get(id=foreign_author_id)
        
        if local_author.host != foreign_author.host:
            # TODO: handle remote host inbox object: https://uofa-cmput404.github.io/general/project.html#friendfollow-request
            pass 
        else:
            pass
            # request is between local authors


### OLD VIEWS ###

# @api_view(["POST"])
# @csrf_exempt
# def follow(request, target_author_id:int): 

#     session_valid = validate_login_session(request)
#     if isinstance(session_valid, Response):
#         return session_valid

#     author_id = request.session["id"]
    
#     if not check_authors_exist(author_id, target_author_id):
#         return Response({
#             "message": "Author does not exist"
#         }, status=404)

#     if Following.objects.filter(author__id=author_id, target_author__id=target_author_id).exists(): 
#         return Response({
#             "message": "Conflict: Author is already following"
#         }, status=409)

#     if FollowingRequest.objects.filter(author__id=author_id, 
#         target_author__id=target_author_id).exists():
#             return Response({
#                 "message": "Conflict: Outstanding request in existence"
#             }, status=409)

#     FollowingRequest.objects.create(
#         author_id=author_id, target_author_id=target_author_id
#     )

#     return Response({"message": "Created: Follow Request"}, status=201)

# @api_view(["POST"])
# @csrf_exempt
# def accept_follow(request, follow_req_id:int):
    
#     session_valid = validate_login_session(request)
#     if isinstance(session_valid, Response):
#         return session_valid
    
#     author_id = request.session["id"]
#     if not check_authors_exist(author_id):
#         return Response({
#             "message": "Author does not exist"
#         }, status=404) 
    
#     if not FollowingRequest.objects.filter(id=follow_req_id).exists(): 
#             return Response({
#                 "message": "Not Available: No pending follow request"
#             }, status=409)

#     try:
#         follow_request = FollowingRequest.objects.get(id=follow_req_id, target_author_id=author_id)
#         Following.objects.create(
#             author_id=follow_request.author_id,
#             target_author_id=author_id
#         )
#         follow_request.delete()
#         return Response({"message": "Follow Accepted"}, status=201)
    
#     except Exception as e:
#         return Response({"message": f"Internal Server Error: Follow could not be accepted {e}"}, status=500)
         

# @api_view(["POST"])
# @csrf_exempt
# def unfollow(request, target_author_id:int):
 
#     session_valid = validate_login_session(request)
#     if isinstance(session_valid, Response):
#         return session_valid
    
#     author_id = request.session["id"]
    
#     if not check_authors_exist(author_id, target_author_id):
#         return Response({
#             "message": "Author does not exist"
#         }, status=404) 
    
#     if not Following.objects.filter(author__id=author_id, target_author__id=target_author_id).exists(): 
#         return Response({
#             "message": "Not Available: Author is not following"
#         }, status=409)

#     Following.objects.delete(
#         author_id=author_id, target_author_id=target_author_id
#     )

#     return Response({"message": "Created: Follow Request"}, status=201)

# @api_view(["GET"])
# def get_follow_requests(request, author_id:int):
    
#     # get all follow requests where the source author is the query parameter 
#     following_reqs = FollowingRequest.objects.filter(target_author_id=author_id)
    
#     serializer = FollowingRequestSerializer(following_reqs, many=True)
#     return Response(serializer.data)

# @api_view(["GET"])
# def get_following(request, author_id:int):
    
#     # get all follow requests where the source author is the query parameter 
#     following = Following.objects.filter(author_id=author_id)
 
#     serializer = FollowingSerializer(following)
#     return Response(serializer.data)

# @api_view(["GET"])
# def get_followers(request, author_id:int):
    
#     # get all follow requests where the source author is the query parameter 
#     following = Following.objects.filter(target_author_id=author_id)
 
#     serializer = FollowingSerializer(following)
#     return Response(serializer.data)