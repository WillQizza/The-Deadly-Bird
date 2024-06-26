from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpRequest
from .models import Like
from posts.models import Post, Comment
from rest_framework.response import Response
from rest_framework import serializers
from deadlybird.serializers import GenericErrorSerializer
from deadlybird.permissions import RemoteOrSessionAuthenticated
from deadlybird.settings import SITE_HOST_URL
from deadlybird.util import resolve_remote_route, get_host_from_api_url, compare_domains
from nodes.util import get_auth_from_host
from identity.models import Author
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from .serializers import LikeSerializer, APIDocsLikeManySerializer
import requests


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
@permission_classes([RemoteOrSessionAuthenticated])
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
    

    # If this is a remote author post, then just redirect.
    if not compare_domains(get_host_from_api_url(author_post.source), SITE_HOST_URL):
        # Fetch from origin node
        author_id, _, post_id = author_post.origin.split("/")[-3:]
        url = resolve_remote_route(get_host_from_api_url(author_post.source), "comment_likes", {
            "author_id": author_id,
            "post_id": post_id,
            "comment_id": comment_id
        })

        auth = get_auth_from_host(get_host_from_api_url(author_post.origin))
        res = requests.get(url=url, auth=auth)
        return Response(res.json(), status=res.status_code)

    # This is a local post
    # Get comment and its likes
    comment = Comment.objects.filter(id=comment_id)\
        .first()

    likes = Like.objects.all()\
        .filter(content_type=Like.ContentType.COMMENT)\
        .filter(content_id=comment.id)\
        .order_by("id")
    
    # Paginate and return serialized result
    serialized_likes = LikeSerializer(likes, many=True)
    return Response(serialized_likes.data)

@extend_schema(
    methods=["GET"],
    responses=APIDocsLikeManySerializer,
    parameters=[
        OpenApiParameter("author_id", type=str, location=OpenApiParameter.PATH, required=True, description="Author id of the post"),
        OpenApiParameter("post_id", type=str, location=OpenApiParameter.PATH, required=True, description="Post id to retrieve likes from"),
    ]
)
@api_view(["GET"])
@permission_classes([RemoteOrSessionAuthenticated])
def post_likes(request: HttpRequest, author_id: str, post_id: str):
    """
    author_id:   author of post_id
    post_id:     post id to retreive likes from
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    """ 
    if request.method == "GET":        
        # Get the post specified by the url 
        author_post = Post.objects\
            .filter(id=post_id, author=author_id)\
            .first()

        if author_post is None:
            return Response({
                "error": True,
                "message": "author post not found"
            }, 404)

        if not compare_domains(author_post.source, SITE_HOST_URL):
            # Fetch from source node
            author_id, _, post_id = author_post.source.split("/")[-3:]
            url = resolve_remote_route(get_host_from_api_url(author_post.source), "post_likes", {
                "author_id": author_id,
                "post_id": post_id
            })
            print("CHECKING ERROR THING")
            print(url)

            auth = get_auth_from_host(get_host_from_api_url(author_post.source))
            print(auth)
            res = requests.get(url=url, auth=auth)
            print(res.status_code)
            likes_json = res.json()
            print(likes_json)
            return Response(likes_json, status=res.status_code)
                
        # Get the likes for the post
        likes = Like.objects.all()\
            .filter(content_type=Like.ContentType.POST)\
            .filter(content_id=author_post.id)\
            .order_by('id')

        # return serialized results
        serialized_likes = LikeSerializer(likes, many=True)
        return Response({
            "type": "Likes",
            "items": serialized_likes.data
        })

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
@permission_classes([RemoteOrSessionAuthenticated])
def liked(request: HttpRequest, author_id: str):
    """
    author_id: author to get all likes originating from
    URL: ://service/authors/{AUTHOR_ID}/liked 
    """

    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response({
            "type": "liked",
            "items": []
        })
    
    if not compare_domains(author.host, SITE_HOST_URL):
        # Remote author. Forward request
        url = resolve_remote_route(author.host, "liked", {
            "author_id": author.id
        })
        auth = get_auth_from_host(author.host)
        response = requests.get(
            url=url,
            auth=auth
        )

        return Response(response.json(), status=response.status_code)

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
