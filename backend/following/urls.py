from django.urls import path

from . import views

urlpatterns = [

     path("authors/<int:author_id>/followers",
          view=views.followers, name="followers"),

     path("authors/<int:author_id>/following",
          view=views.following, name="following"),

     path("authors/<int:author_id>/followers/<int:foreign_author_id>", 
          views.modify_follower, name="modify_follower"),
    
     path("authors/request-follower/<int:local_author_id>/<int:foreign_author_id>",
          views.request_follower, name="request_follower")
]