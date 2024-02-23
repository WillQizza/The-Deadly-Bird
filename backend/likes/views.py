from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpRequest
from .models import Like
from posts.models import Post
from rest_framework.response import Response

@api_view(["GET", "POST"])
def post_likes(request: HttpRequest, author_id: int, post_id: int):
    """
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    """ 
    if request.method == "GET":        
        # get the post specified by the url 
        author_post = Post.objects.filter(author_id=author_id, id=post_id).first()

        if author_post is None:
            return Response({
                "message": "Author post not Found"
            }, 404)

        # get all likes from other authors on post 
        foreign_likes = Like.objects.filter(
            content_type=Like.ContentType.POST,
            content_id=author_post.id,
        )

        print(foreign_likes)
        return Response({
            "Ok": True
        }, status=200)

    elif request.mehthod == "POST":
        # create like object
        pass

@api_view(["GET"])
def liked(request: HttpRequest, author_id: int):
    """
    Get all the liked public things which author_id has liked.
    """
    