import base64
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from following.util import is_friends
from deadlybird.pagination import Pagination
from .serializers import PostSerializer
from .models import Post, Author, Following
from django.db.models import Q
from .util import send_post_to_inboxes

@api_view(["GET", "POST"])
def posts(request: HttpRequest, author_id: str):
  if request.method == "GET":
    # Retrieve author posts
    # Create paginator
    paginator = Pagination("posts")

    # Check if the person has access to friend posts
    can_see_friends = False
    if "id" in request.session:
      can_see_friends = (author_id == request.session["id"]) or \
                          is_friends(author_id, request.session["id"])
      
    # Retrieve ordered posts that should be shown
    if can_see_friends:
      posts = Post.objects.all().filter(author=author_id)

      can_see_unlisted = author_id == request.session["id"]
      if not can_see_unlisted:
        posts = posts.exclude(visibility=Post.Visibility.UNLISTED) \
      
      posts = posts.order_by("-published_date")
    else:
      posts = Post.objects.all() \
                .filter(author=author_id, visibility=Post.Visibility.PUBLIC) \
                .order_by("-published_date")
    
    # Paginate and serialize results
    posts_on_page = paginator.paginate_queryset(posts, request)
    serialized_posts = PostSerializer(posts_on_page, many=True)

    return paginator.get_paginated_response(serialized_posts.data)
  else:
    # Create author post
    # Check the request body for all the required fields
    if (not "title" in request.POST) \
      or (not "description" in request.POST) \
      or (not "contentType" in request.POST) \
      or (not "content" in request.POST) \
      or (not "visibility" in request.POST):
      return Response({
        "error": True,
        "message": "Required field missing."
      }, status=400)
    
    # Check that the request body contains valid data
    if not (0 < len(request.POST["title"]) <= 255) \
      or not (0 < len(request.POST["description"]) <= 255) \
      or not (request.POST["contentType"] in Post.ContentType.values) \
      or not (request.POST["visibility"] in Post.Visibility.values):
      return Response({
        "error": True,
        "message": "Request body does not match required schema."
      }, status=400)
    
    # Check that we are who we say we are
    if (not "id" in request.session) \
      or (request.session["id"] != author_id):
      return Response({
        "error": True,
        "message": "You do not have permission to post as this user."
      }, status=401)

    # Create the post
    author = get_object_or_404(Author, id=author_id)

    post = Post.objects.create(
      title=request.POST["title"],
      description=request.POST["description"],
      content_type=request.POST["contentType"],
      content=request.POST["content"],
      author=author,
      visibility=request.POST["visibility"]
    )
    
    # Add post creation notification to relevant inboxes
    send_post_to_inboxes(post.id, author_id)

    return Response({
      "error": False,
      "message": "Post created successfully."
    }, status=201)

@api_view(["GET", "DELETE", "PUT"])
def post(request: HttpRequest, author_id: str, post_id: str):
  if request.method == "GET":
    # Check if the person has access to friend posts
    can_see_friends = False
    if "id" in request.session:
      can_see_friends = (author_id == request.session["id"]) or \
                          is_friends(author_id, request.session["id"])
      
    # Retrieve posts that should be shown
    try:
      if can_see_friends:
        post = Post.objects.get(id=post_id, author=author_id)
      else:
        post = Post.objects.get(
            Q(id=post_id, author=author_id, visibility=Post.Visibility.PUBLIC) |
            Q(id=post_id, author=author_id, visibility=Post.Visibility.UNLISTED)
        )
    except:
      return Response({
        "error": True,
        "message": "Post not found."
      }, status=404)
    
    # Return serialized result
    serialized_post = PostSerializer(post)

    return Response(serialized_post.data)
  elif request.method == "DELETE":
    # Delete a single post. Can be initiated by local or remote host.
    print("recieved delete:", author_id, post_id)
    # Get post
    post = Post.objects.filter(id=post_id).first()
    # Check if post exists
    if post is None:
      return Response({"error": True, "message": "post not found"}, status=404)
    # Delete post
    try: 
      post.delete()
      return Response({"error": False, "message": "post deleted"}, status=204)
    except Exception as e:
      print(e)
      return Response({"error": True, "message": "Server error, failed to delete"}, status=500)

  elif request.method == "PUT":
    # Edit a post
    # Check the request body for all the required fields
    if (not "title" in request.POST) \
      or (not "description" in request.POST) \
      or (not "contentType" in request.POST) \
      or (not "content" in request.POST) \
      or (not "visibility" in request.POST):
      return Response({
        "error": True,
        "message": "Required field missing."
      }, status=400)
    
    # Check that the request body contains valid data
    if not (0 < len(request.POST["title"]) <= 255) \
      or not (0 < len(request.POST["description"]) <= 255) \
      or not (request.POST["contentType"] in Post.ContentType.values) \
      or not (request.POST["visibility"] in Post.Visibility.values):
      return Response({
        "error": True,
        "message": "Request body does not match required schema."
      }, status=400)
    
    # Check that we are who we say we are
    if (not "id" in request.session) \
      or (request.session["id"] != author_id):
      return Response({
        "error": True,
        "message": "You do not have permission to edit posts as this user."
      }, status=401)
    
    # Check that the post exists
    try:
      post = Post.objects.get(id=post_id)
    except:
      return Response({
        "error": True,
        "message": "Post not found."
      }, status=404)
    
    # Check that the post belongs to us
    if post.author.id != author_id:
      return Response({
        "error": True,
        "message": "You do not have permission to edit this post."
      }, status=404)

    # Update the post
    post.title = request.POST["title"]
    post.description = request.POST["description"]
    post.content_type = request.POST["contentType"]
    post.visibility = request.POST["visibility"]
    post.save()

    return Response({
      "error": False,
      "message": "Post updated successfully."
    }, status=200)

@api_view(["GET"])
def post_image(_: HttpRequest, author_id: str, post_id: str):
  # Retrieve post image
  post = get_object_or_404(Post, id=post_id)
  return HttpResponse(base64.b64decode(post.content), content_type="image/*")

@api_view(["GET"])
def post_stream(request: HttpRequest, stream_type: str):
  # Public stream
  if stream_type == "public":
    paginator = Pagination("posts")

    # Get all public posts
    posts = Post.objects.all() \
      .filter(visibility=Post.Visibility.PUBLIC) \
      .order_by("-published_date")
    
    # Paginate and return serialized result
    posts_on_page = paginator.paginate_queryset(posts, request)
    serialized_posts = PostSerializer(posts_on_page, many=True)

    return paginator.get_paginated_response(serialized_posts.data)
  
  # Following stream
  elif stream_type == 'following':
    paginator = Pagination("posts")

    # Get all authors following
    following = Following.objects.all() \
        .filter(author=request.session["id"]) \
        .values_list('target_author', flat=True)

    # Get all not friends from those following
    not_friends = [follow for follow in following if not is_friends(int(follow), int(request.session["id"]))]

    # Get all posts all posts from authors following
    posts = Post.objects.all() \
        .filter(author__in=following) \
        .exclude(visibility=Post.Visibility.UNLISTED) \
        .exclude(visibility=Post.Visibility.FRIENDS, author__in=not_friends) \
        .order_by("-published_date")
    
    # Paginate and return serialized result
    posts_on_page = paginator.paginate_queryset(posts, request)
    serialized_posts = PostSerializer(posts_on_page, many=True)

    return paginator.get_paginated_response(serialized_posts.data)
  
  # Invalid stream
  else:
    return Response({
      "error": True,
      "message": "Invalid stream type."
    }, status=404)
