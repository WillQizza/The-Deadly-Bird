from django.urls import path

from . import views

urlpatterns = [
  path("authors/<str:author_id>/posts/", views.posts, name="posts"),
  path("authors/<str:author_id>/posts/<str:post_id>/", views.post, name="post"),
  path("authors/<str:author_id>/posts/<str:post_id>/image/", views.post_image, name="post_image"),
  path("posts/<str:stream_type>/", views.post_stream, name="post_stream"),
]
