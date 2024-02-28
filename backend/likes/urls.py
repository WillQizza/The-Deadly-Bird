from django.urls import path

from . import views

urlpatterns = [
    path("authors/<str:author_id>/posts/<str:post_id>/likes/", 
        view=views.post_likes, name="post_likes"),
    
    path("authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/likes/", 
        view=views.comment_likes, name="comment_likes"),

    path("authors/<str:author_id>/liked/",
         view=views.liked, name="liked")
]