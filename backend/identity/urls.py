from django.urls import path

from . import views

urlpatterns = [
  path("authors/", view=views.authors, name="authors"),
  path("authors/<str:author_id>/", view=views.author, name="author"),
  path("login/", view=views.login, name="login"),
  path("register/", view=views.register),
  path("update/", view=views.update, name="update"),
  path("authors/<str:author_id>/inbox", view=views.inbox, name="inbox")
]