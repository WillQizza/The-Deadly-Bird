import base64
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer, OpenApiTypes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from deadlybird.serializers import GenericSuccessSerializer, GenericErrorSerializer
from deadlybird.settings import SITE_HOST_URL
from deadlybird.pagination import Pagination, generate_pagination_schema, generate_pagination_query_schema
from deadlybird.permissions import RemoteOrSessionAuthenticated, SessionAuthenticated, RemoteNodeAuthenticated, IsGetRequest, IsPutRequest, IsPostRequest, IsDeleteRequest
from deadlybird.util import generate_full_api_url, generate_next_id, resolve_remote_route, get_host_from_api_url, compare_domains
from following.util import is_friends
from likes.models import Like
from identity.models import InboxMessage, BlockedAuthor
from nodes.util import get_auth_from_host
from .models import Post, Author, Following, Comment, FollowingFeedPost
from .serializers import CommentSerializer, PostSerializer
from .util import send_post_to_inboxes
from .pagination import CommentsPagination, generate_comments_pagination_schema, generate_comments_pagination_query_schema
import requests
import json

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
@permission_classes([(IsGetRequest & RemoteOrSessionAuthenticated) | (IsPostRequest & SessionAuthenticated)])
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

    id = generate_next_id()
    post = Post.objects.create(
      id=id,
      title=request.POST["title"],
      origin=generate_full_api_url("post", kwargs={ "author_id": author.id, "post_id": id }),
      source=generate_full_api_url("post", kwargs={ "author_id": author.id, "post_id": id }),
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
@permission_classes([ RemoteOrSessionAuthenticated ])
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
      # Delete all likes associated with the post 
      likes = Like.objects.all().filter(content_id=post.id, content_type=Like.ContentType.POST)
      for like in likes:
        like.delete()

      # Delete all likes associated with the comments of this post
      comments = Comment.objects.all().filter(post=post)
      for comment in comments:
        likes = Like.objects.all().filter(content_id=comment.id, content_type=Like.ContentType.COMMENT)
        for like in likes:
          like.delete()

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
    post.content = request.POST["content"]
    post.save()

    return Response({
      "error": False,
      "message": "Post updated successfully."
    }, status=200)

@extend_schema(
    methods=["POST"],
    request=None,
    responses={
      200: PostSerializer,
      400: GenericErrorSerializer,
      401: GenericErrorSerializer,
      404: GenericErrorSerializer
    }
)
@api_view(["POST"])
@permission_classes([ SessionAuthenticated ])
def share_post(request: HttpRequest, author_id: str, post_id: str):
  try:
    post = Post.objects.get(id=post_id)
  except Post.DoesNotExist:
    return Response({
      "error": True,
      "message": "Post could not be found."
    }, status=404)
  
  if post.visibility != Post.Visibility.PUBLIC:
    return Response({
      "error": True,
      "message": "Cannot share a non-public post"
    }, status=400)
  
  author = Author.objects.get(id=request.session["id"])

  origin_author = post.origin_author if post.origin_author != None else post.author

  # Create a copy of the post that we can share
  shared_post_id = generate_next_id()
  shared_post = Post.objects.create(
    id=shared_post_id,
    title=post.title,
    source=generate_full_api_url("post", kwargs={ "author_id": author.id, "post_id": shared_post_id }), # This is modified anyway on send_post_to_inboxes
    origin=post.origin,
    description=post.description,
    content_type=post.content_type,
    content=post.content,
    author=author,
    origin_author=origin_author,
    visibility=post.visibility
  )
  
  send_post_to_inboxes(shared_post.id, author.id)
  return Response(PostSerializer(shared_post).data, status=201)

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
@permission_classes([ RemoteOrSessionAuthenticated ])
def post_stream(request: HttpRequest, stream_type: str):
  # Public stream
  if stream_type == "public":
    paginator = Pagination("posts")

    # Get all public posts

    blocked_authors = []
    if "id" in request.session:
      blocked_authors = list(map(lambda b: b.blocked_author, list(BlockedAuthor.objects.filter(author=request.session["id"]))))

    posts = Post.objects.all() \
      .filter(visibility=Post.Visibility.PUBLIC) \
      .exclude(Q(author__in=blocked_authors) | Q(origin_author__in=blocked_authors)) \
      .order_by("-published_date")
      

    if hasattr(request, "is_node_authenticated") and request.is_node_authenticated:
      posts = posts.filter(origin__startswith=SITE_HOST_URL)

    # Paginate and return serialized result
    posts_on_page = paginator.paginate_queryset(posts, request)
    serialized_posts = PostSerializer(posts_on_page, many=True)

    return paginator.get_paginated_response(serialized_posts.data)
  
  # Following stream
  elif stream_type == 'following' and "id" in request.session:
    paginator = Pagination("posts")

    # Get all authors following
    following = Following.objects.all() \
        .filter(author=request.session["id"]) \
        .values_list('target_author', flat=True)

    # Get all not friends from those following
    not_friends = [follow for follow in following if not is_friends(follow, request.session["id"])]

    blocked_authors = list(map(lambda b: b.blocked_author, list(BlockedAuthor.objects.filter(author=request.session["id"]))))

    # Get all posts all posts from authors following
    feed_messages = FollowingFeedPost.objects.filter(from_author__in=following, follower_id=request.session["id"]).order_by("-published_date") \
      .exclude(post__visibility=Post.Visibility.UNLISTED) \
      .exclude(post__visibility=Post.Visibility.FRIENDS, from_author__in=not_friends) \
      .exclude(post__origin_author__in=blocked_authors)
    
    # paginate results
    feed_messages_on_page = paginator.paginate_queryset(feed_messages, request)
    posts = list(map(lambda fm: fm.post, feed_messages_on_page))
    
    # return serialized result
    serialized_posts = PostSerializer(posts, many=True)

    return paginator.get_paginated_response(serialized_posts.data)
  
  # Invalid stream
  else:
    return Response({
      "error": True,
      "message": "Invalid stream type."
    }, status=404)

@extend_schema(
  parameters=[
    OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id of the post"),
    OpenApiParameter("post_id", type=str, location=OpenApiParameter.PATH, required=True, description="Post id of the post to interact with")
  ]
)
@extend_schema(
  operation_id="api_authors_retrieve_all_post_comments",
  methods=["GET"],
  parameters=[
    *generate_comments_pagination_query_schema()
  ],
  responses=generate_comments_pagination_schema()
)
@extend_schema(
  operation_id="api_authors_create_new_post_comment",
  methods=["POST"],
  request=PostCreationPayloadSerializer,
  responses={
    201: GenericSuccessSerializer,
    400: GenericErrorSerializer,
    404: GenericErrorSerializer
  }
)
@api_view(["GET", "POST"])
@permission_classes([ RemoteOrSessionAuthenticated ])
def comments(request: HttpRequest, author_id: str, post_id: str):
  # Check if the person has access to friend posts
  can_see_friends = False
  if "id" in request.session:
    can_see_friends = (author_id == request.session["id"]) or \
                        is_friends(author_id, request.session["id"])
  
  # Retrieve post, if allowed
  try:
    if can_see_friends:
      post = Post.objects.get(
        id=post_id, author=author_id
      )
    else:
      post = Post.objects.get(
          Q(id=post_id, author=author_id, visibility=Post.Visibility.PUBLIC) |
          Q(id=post_id, author=author_id, visibility=Post.Visibility.UNLISTED)
      )
  except Post.DoesNotExist:
    return Response({
      "error": True,
      "message": "Post not found."
    }, status=404)
  
  if request.method == "GET":
    # Get the comments on the post

    if not compare_domains(post.origin, SITE_HOST_URL):
      # Remote post. get comments from remote
      origin_aid, _, origin_pid = post.origin.split("/")[-3:]
      url = resolve_remote_route(get_host_from_api_url(post.origin), "comments", {
          "author_id": origin_aid,
          "post_id": origin_pid
      })

      auth = get_auth_from_host(get_host_from_api_url(post.origin))

      res = requests.get(url=url, auth=auth, params=request.GET.dict())
      return Response(res.json(), status=res.status_code)

    comments = Comment.objects.all() \
          .filter(post=post) \
          .order_by("-published_date")
    
    # Paginate the comments
    paginator = CommentsPagination()
    comments_on_page = paginator.paginate_queryset(comments, request)
    serialized_comments = CommentSerializer(comments_on_page, many=True)

    # Return the serialized comments
    return paginator.get_paginated_response(post_id, serialized_comments.data)
  
  else:
    # Add a comment to post
    # Check the request body for all the required fields
    if (not "comment" in request.POST) \
      or (not "contentType" in request.POST):
      return Response({
        "error": True,
        "message": "Required field missing."
      }, status=400)
    
    # Check that the request body contains valid data
    if not (request.POST["contentType"] in Comment.ContentType.values) \
      or not (len(request.POST["comment"]) > 0):
      return Response({
        "error": True,
        "message": "Request body does not match required schema."
      }, status=400)
    
    author = get_object_or_404(Author, id=request.session["id"])

    # Check if the post is a remote post or not
    if not compare_domains(post.origin, SITE_HOST_URL):
      # Remote post
      remote_author = post.author
      url = resolve_remote_route(remote_author.host, "inbox", {
          "author_id": remote_author.id
      })

      comment = Comment.objects.create(
        post=post,
        author=author,
        content_type=request.POST["contentType"],
        content=request.POST["comment"]
      )
      payload = CommentSerializer(comment).data

      auth = get_auth_from_host(remote_author.host)
      response = requests.post(
        url=url,
        headers={'Content-Type': 'application/json'}, 
        data=json.dumps(payload), 
        auth=auth
      )

      # Print error if response failed
      if not response.ok:
        return Response({"error": True, "message": "Failed to create comment"}, status=response.status_code)
    else:

      # Send inbox message to post's owner
      if compare_domains(post.author.host, SITE_HOST_URL):
        # Local post
        comment = Comment.objects.create(
          post=post,
          author=author,
          content_type=request.POST["contentType"],
          content=request.POST["comment"]
        )
        InboxMessage.objects.create(
            author=comment.post.author,
            content_id=comment.id,
            content_type=InboxMessage.ContentType.COMMENT
        )
      else:
        # Remote post
        comment = Comment.objects.create(
          post=post,
          author=author,
          content_type=request.POST["contentType"],
          content=request.POST["comment"]
        )
        payload = CommentSerializer(comment).data

        # The original author did not originate from our node... What's the source for this post?
        # Find the quickest post to get to the origin
        earliest_non_remote_post = Post.objects.all().filter(origin=post.origin).order_by("published_date").first()
        source_author = earliest_non_remote_post.author
        
        url = resolve_remote_route(source_author.host, "inbox", {
          "author_id": source_author.id
        })

        auth = get_auth_from_host(source_author.host)
        response = requests.post(
          url=url,
          headers={'Content-Type': 'application/json'}, 
          data=json.dumps(payload), 
          auth=auth
        )

        if not response.ok:
          return Response({"error": True, "message": "Failed to create comment"}, status=response.status_code)


    return Response({
      "error": False,
      "message": "Comment created successfully."
    }, status=201)