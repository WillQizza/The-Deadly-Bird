from django.urls import path

from . import views

urlpatterns = [
  path("authors/", view=views.authors),
  path("authors/<int:author_id>/", view=views.author),
  path("login/", view=views.login, name="login"),
  path("register/", view=views.register),
  path("authors/<int:author_id>/inbox", view=views.inbox, name="inbox")
]