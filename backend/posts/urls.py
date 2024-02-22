from django.urls import path

from . import views

urlpatterns = [
  path("authors/<int:author_id>/posts/", views.posts, name="posts"),
  path("authors/<int:author_id>/posts/<int:post_id>", views.post, name="post"),
  path("posts/<str:stream_type>", views.post_stream, name="post_stream"),
]
