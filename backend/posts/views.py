import base64
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from deadlybird.serializers import GenericSuccessSerializer, GenericErrorSerializer
from deadlybird.pagination import Pagination, generate_pagination_schema, generate_pagination_query_schema
from deadlybird.util import generate_full_api_url
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer, OpenApiTypes
from following.util import is_friends
from .serializers import PostSerializer
from .models import Post, Author, Following
from django.db.models import Q
from .util import send_post_to_inboxes

PostCreationPayloadSerializer = inline_serializer("PostCreationPayload", fields={
  "title": serializers.CharField(),
  "description": serializers.CharField(),
  "contentType": serializers.CharField(),
  "content": serializers.CharField(),
  "visibility": serializers.CharField(),
})
@extend_schema(
  parameters=[
    OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id to interact with")
  ]
)
@extend_schema(
  operation_id="api_authors_retrieve_all_posts",
  methods=["GET"],
  parameters=[
    *generate_pagination_query_schema()
  ],
  responses=generate_pagination_schema("posts", PostSerializer(many=True))
)
@extend_schema(
  operation_id="api_authors_create_new_post",
  methods=["POST"],
  request=PostCreationPayloadSerializer,
  responses={
    201: GenericSuccessSerializer,
    400: GenericErrorSerializer,
    401: GenericErrorSerializer
  }
)
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
      origin=generate_full_api_url("api"),
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

@extend_schema(
    parameters=[
        OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id of the post"),
        OpenApiParameter("post_id", type=str, location=OpenApiParameter.PATH, required=True, description="Post id to interact with")
    ]
)
@extend_schema(
    methods=["GET"],
    responses={
      404: GenericErrorSerializer,
      200: PostSerializer()
    }
)
@extend_schema(
  methods=["DELETE"],
  responses={
    404: GenericErrorSerializer,
    500: GenericErrorSerializer,
    204: GenericSuccessSerializer
  }
)
@extend_schema(
  methods=["PUT"],
  request=PostCreationPayloadSerializer,
  responses={
    200: GenericSuccessSerializer,
    400: GenericErrorSerializer,
    401: GenericErrorSerializer
  }
)
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

@extend_schema(
    parameters=[
        OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id of the post"),
        OpenApiParameter("post_id", type=str, location=OpenApiParameter.PATH, required=True, description="Post id to retrieve image of")
    ],
    responses={
      (200, "image/*"): OpenApiTypes.BINARY,
      404: GenericErrorSerializer,
      400: GenericErrorSerializer
    }
)
@api_view(["GET"])
def post_image(_: HttpRequest, author_id: str, post_id: str):
  # Retrieve post image
  try:
    post = Post.objects.get(id=post_id)
  except Post.DoesNotExist:
    return Response({
      "error": True,
      "message": "Post could not be found."
    }, status=404)

  if (post.content_type != Post.ContentType.APPLICATION_BASE64) \
    and (post.content_type != Post.ContentType.JPEG_BASE64) \
    and (post.content_type != Post.ContentType.PNG_BASE64):
      return Response({
        "error": True,
        "message": "This post is not an image post."
      }, status=400)

  return HttpResponse(base64.b64decode(post.content), content_type="image/*")

@extend_schema(
    parameters=[
        OpenApiParameter("stream_type", type=str, location=OpenApiParameter.PATH, required=True, description="Either \"following\" or \"public\""),
        *generate_pagination_query_schema()
    ],
    responses={
      200: generate_pagination_schema("posts", PostSerializer(many=True)),
      404: GenericErrorSerializer
    }
)
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
    not_friends = [follow for follow in following if not is_friends(follow, request.session["id"])]

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
