from django.urls import reverse
from django.conf import settings
import secrets

def generate_next_id():
  return secrets.token_urlsafe(10)

def generate_full_api_url(view: str, kwargs: dict[str, str] = None):
  if settings.SITE_HOST_URL.endswith("/"):
    return settings.SITE_HOST_URL + reverse(view, kwargs=kwargs)[1:]
  else:
    return settings.SITE_HOST_URL + reverse(view, kwargs=kwargs)