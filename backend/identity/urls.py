from django.urls import path

from . import views

urlpatterns = [
  path("authors/", view=views.authors, name="authors"),
  path("authors/<str:author_id>/", view=views.author, name="author"),
  path("login/", view=views.login, name="login"),
  path("register/", view=views.register),
  path("logout/", view=views.logout, name="logout"),
  path("authors/<str:author_id>/inbox", view=views.inbox, name="inbox"),
  path("authors/<str:author_id>/inbox/", view=views.inbox, name="inbox2") # Our GET inbox seems to failure otherwise?
]