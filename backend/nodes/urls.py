from django.urls import path
from . import views

urlpatterns = [
    path("hostname/", view=views._getHostname, name="hostname"),
]