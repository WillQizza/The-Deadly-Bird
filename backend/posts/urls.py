from django.urls import path

from . import views

urlpatterns = [
  path("authors/<str:author_id>/posts/", views.posts, name="posts"),
  path("authors/<str:author_id>/posts/<str:post_id>", views.post, name="post"),
]
