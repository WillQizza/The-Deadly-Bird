from django.urls import path

from . import views

urlpatterns = [
    path("authors/<str:author_id>/posts/<str:post_id>/likes", 
        view=views.post_likes, name="post_likes"),
    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    # path("authors/<int:author_id>/posts/<int:post_id>/likes", 
    #     view=views.post_likes, name="post_likes"),

    path("authors/<str:author_id>/liked",
         view=views.liked, name="liked")
]