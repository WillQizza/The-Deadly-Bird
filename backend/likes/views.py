from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpRequest
from .models import Like
from posts.models import Post, Comment
from rest_framework.response import Response
from rest_framework import serializers
from deadlybird.pagination import Pagination, generate_pagination_schema, generate_pagination_query_schema
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from .serializers import LikeSerializer
from identity.models import InboxMessage

@extend_schema(
        responses={
            404: inline_serializer("CommentLikes404", fields={ "message": serializers.CharField() }),
            200: generate_pagination_schema("likes", LikeSerializer(many=True))
        },
        parameters=[
            OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id of the post"),
            OpenApiParameter("post_id", type=str, location=OpenApiParameter.PATH, required=True, description="Post id to retrieve comments from"),
            OpenApiParameter("comment_id", type=str, location=OpenApiParameter.PATH, required=True, description="Comment id to retrieve likes from"),
            *generate_pagination_query_schema()
        ]
)
@api_view(["GET"])
def comment_likes(request: HttpRequest, author_id: str, post_id: str, comment_id: str):
    """
    author_id:   author of post_id
    post_id:     post of author to get comment from
    comment_id:  comment to get likes from
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    """
    # Get author's post
    author_post = Post.objects.filter(id=post_id, author_id=author_id)\
        .first()
    
    if author_post is None:
        return Response({
            "message": "Author post not Found"
        }, 404)
    
    # Get comment and its likes
    comment = Comment.objects.filter(post_id=author_post.id, author_id=author_id)\
        .first()

    likes = Like.objects.all()\
        .filter(content_type=Like.ContentType.COMMENT)\
        .filter(content_id=comment.id)\
        .order_by("id")
    
    # Paginate and return serialized result
    paginator = Pagination("likes")
    likes_page = paginator.paginate_queryset(likes, request)
    serialized_likes = LikeSerializer(likes_page, many=True)

    return paginator.get_paginated_response(serialized_likes.data)

LikePostErrorSerializer = inline_serializer("LikePostError", fields={ 
            "error": serializers.BooleanField(default=True), 
            "message": serializers.CharField() 
        })
@extend_schema(
    parameters=[
        OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id of the post"),
        OpenApiParameter("post_id", type=str, location=OpenApiParameter.PATH, required=True, description="Post id to retrieve likes from")
    ]
)
@extend_schema(
    methods=["GET"],
    responses=generate_pagination_schema("likes", LikeSerializer(many=True)),
    parameters=[
        OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id of the post"),
        OpenApiParameter("post_id", type=str, location=OpenApiParameter.PATH, required=True, description="Post id to retrieve likes from"),
        *generate_pagination_query_schema()
    ]
)
@extend_schema(
    methods=["POST"],
    request=None,
    responses={
        200: inline_serializer("LikePostSuccess", fields={ 
            "error": serializers.BooleanField(default=False), 
            "message": serializers.CharField() 
        }),
        404: LikePostErrorSerializer,
        409: LikePostErrorSerializer,
        500: LikePostErrorSerializer,
    }
)
@api_view(["GET", "POST"])
def post_likes(request: HttpRequest, author_id: str, post_id: str):
    """
    author_id:   author of post_id
    post_id:     post id to retreive likes from
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    """ 
    if request.method == "GET":        
        # Get the post specified by the url 
        author_post = Post.objects\
            .filter(id=post_id, author_id=author_id)\
            .first()

        if author_post is None:
            return Response({
                "message": "author post not Found"
            }, 404)
        
        # Get the likes for the post
        likes = Like.objects.all()\
            .filter(content_type=Like.ContentType.POST)\
            .filter(content_id=author_post.id)\
            .order_by('id')

        # Paginate and return serialized results
        paginator = Pagination("likes")
        likes_page = paginator.paginate_queryset(likes, request)
        serialized_likes = LikeSerializer(likes_page, many=True)

        return paginator.get_paginated_response(serialized_likes.data) 

    if request.method == "POST":
        # author_id likes post_id
        # Get the post
        post = Post.objects.filter(id=post_id, author_id=author_id).first()
        if post is None:
            return Response({"error": True,"message": "authors post not found"}, status=404)
        
        # Check if author has already liked the post
        existing_like = Like.objects\
            .filter(send_author_id=author_id, content_id=post.id)\
            .first()
        
        if existing_like is not None:
            return Response({"error": True, "message": "post already liked"}, status=409)

        try:
            # Create the like
            like = Like.objects.create(
                send_author_id=author_id,
                receive_author_id=post.author.id,
                content_id=post.id,
                content_type=Like.ContentType.POST
            )

            # Add notification to author's inbox
            InboxMessage.objects.create(
                author_id=post.author.id,
                content_id=like.id,
                content_type=InboxMessage.ContentType.LIKE
            )

            return Response({"error": False, "message": "like created"}, status=200)
        except:
            return Response({"error": True, "message": "create like failed"}, status=500)
            

@extend_schema(
        responses=generate_pagination_schema("likes", LikeSerializer(many=True)),
        parameters=[
            OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id to lookup likes of"),
            *generate_pagination_query_schema()
        ]
)
@api_view(["GET"])
def liked(request: HttpRequest, author_id: int):
    """
    author_id: author to get all likes originating from
    URL: ://service/authors/{AUTHOR_ID}/liked 
    """
    if request.method == "GET":
        # Get likes
        liked = Like.objects.all()\
            .filter(send_author_id=author_id)\
            .order_by("id")
        
        # Paginate and return serialized results
        paginator = Pagination("likes")
        liked_page = paginator.paginate_queryset(liked, request)
        serialized_liked = LikeSerializer(liked_page, many=True)

        return paginator.get_paginated_response(serialized_liked.data)
    