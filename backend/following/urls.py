from django.urls import path, re_path

from . import views

urlpatterns = [

     path("authors/<str:author_id>/followers",
          view=views.followers, name="followers"),

     path("authors/<str:author_id>/following",
          view=views.following, name="following"),

     re_path(r'^authors/(?P<author_id>[\w-]+)/followers/(?P<foreign_author_id>.*)/$', views.modify_follower, name="modify_follower"),
     re_path(r'^authors/(?P<author_id>[\w-]+)/followers/(?P<foreign_author_id>.*)$', views.modify_follower, name="modify_follower2"),
    
     path("authors/request-follower/<str:author_id>/<str:target_author_id>",
          views.request_follower, name="request_follower")
]