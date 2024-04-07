from django.urls import path

from . import views

urlpatterns = [
  path("subscription/checkout", view=views.checkout, name="subscription_checkout"),
  path("subscription/event", view=views.subscription_event, name="subscription_event"),
  path("subscription/check", view=views.subscription_check, name="subscription_check")
]