from django.urls import path

from . import views

urlpatterns = [
  path("authors/<int:author_id>/", view=views.author),
  path("login/", view=views.login, name="login"),
  path("register/", view=views.register)
]