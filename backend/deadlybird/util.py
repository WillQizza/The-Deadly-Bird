from django.urls import reverse
from django.conf import settings
import secrets

def generate_next_id():
  return secrets.token_urlsafe(10)

def generate_full_api_url(view: str, force_no_slash = False, kwargs: dict[str, str] = None):
  if settings.SITE_HOST_URL.endswith("/"):
    api_url = settings.SITE_HOST_URL + reverse(view, kwargs=kwargs)[1:]
  else:
    api_url = settings.SITE_HOST_URL + reverse(view, kwargs=kwargs)
  
  if force_no_slash and api_url.endswith("/"):
    api_url = api_url[:-1]
  
  return api_url