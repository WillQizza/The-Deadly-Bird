from django.urls import path

from . import views

urlpatterns = [

    # POST routes 
    path("follow/<int:target_author_id>/", view=views.follow),
    path("unfollow/<int:target_author_id>/", view=views.unfollow),
    path("accept_follow/<int:follow_req_id>/", view=views.accept_follow),
    
    # GET routes for data 
    # path("get-followers/<int:author_id>"),
    # path("get-following/<int:author_id>"),
]