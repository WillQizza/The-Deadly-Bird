from django.urls import path

from . import views

urlpatterns = [
  path("authors/<int:author_id>/posts/", views.posts, name="posts")
]