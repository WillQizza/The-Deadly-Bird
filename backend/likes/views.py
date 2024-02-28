from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpRequest
from .models import Like
from posts.models import Post, Comment
from rest_framework.response import Response
from rest_framework import serializers
from deadlybird.serializers import GenericErrorSerializer, GenericSuccessSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from .serializers import LikeSerializer, APIDocsLikeManySerializer
from identity.models import InboxMessage

@extend_schema(
        responses={
            404: GenericErrorSerializer,
            200: APIDocsLikeManySerializer
        },
        parameters=[
            OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id of the post"),
            OpenApiParameter("post_id", type=str, location=OpenApiParameter.PATH, required=True, description="Post id to retrieve comments from"),
            OpenApiParameter("comment_id", type=str, location=OpenApiParameter.PATH, required=True, description="Comment id to retrieve likes from")
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
            "error": True,
            "message": "Author post not Found"
        }, 404)
    
    # Get comment and its likes
    comment = Comment.objects.filter(id=comment_id)\
        .first()

    likes = Like.objects.all()\
        .filter(content_type=Like.ContentType.COMMENT)\
        .filter(content_id=comment.id)\
        .order_by("id")
    
    # Paginate and return serialized result
    serialized_likes = LikeSerializer(likes, many=True)
    return serialized_likes.data

@extend_schema(
    methods=["GET"],
    responses=APIDocsLikeManySerializer,
    parameters=[
        OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id of the post"),
        OpenApiParameter("post_id", type=str, location=OpenApiParameter.PATH, required=True, description="Post id to retrieve likes from"),
    ]
)
@api_view(["GET"])
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
                "error": True,
                "message": "author post not Found"
            }, 404)
        
        # Get the likes for the post
        likes = Like.objects.all()\
            .filter(content_type=Like.ContentType.POST)\
            .filter(content_id=author_post.id)\
            .order_by('id')

        # return serialized results
        serialized_likes = LikeSerializer(likes, many=True)
        return Response(serialized_likes.data)

@extend_schema(
        responses=inline_serializer("Liked", fields={
            "type": serializers.CharField(default="liked", read_only=True),
            "items": APIDocsLikeManySerializer
        }),
        parameters=[
            OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id to lookup likes of")
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
        serialized_liked = LikeSerializer(liked, many=True)

        return Response({
            "type": "liked",
            "items": serialized_liked.data
        })
    