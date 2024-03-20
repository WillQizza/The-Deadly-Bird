from django.urls import reverse
from django.conf import settings
from deadlybird.settings import SITE_HOST_URL
from urllib.parse import urljoin
import secrets
import os

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

def resolve_remote_route(host: str, view: str, kwargs):
  """
  Given the hostname of an author, we may have to swap the hostname to escape
  the dockercontainer and construct a url to the host. Only applicable to local dev.
  """    
  if os.environ.get("DOCKER") is not None:
    host = host.replace("localhost", "host.docker.internal")

  route = reverse(viewname=view, kwargs=kwargs)

  return urljoin(host, route)

def resolve_docker_host(host: str):
  """
  We may need to 
  """    
  if os.environ.get("DOCKER") is not None:
    host = host.replace("host.docker.internal", "localhost")
  
  return host

def get_host_from_api_url(url: str) -> str|None:
  """
  Retrieve the base host associated with the url.
  While hacky, this method will work.
  """
  
  if url.startswith(SITE_HOST_URL):
     return SITE_HOST_URL
  
  if os.environ.get("DOCKER") is not None:
    url = url.replace("localhost", "host.docker.internal")
  
  from nodes.models import Node
  for node in Node.objects.all():
    if url.startswith(node.host):
      return node.host
  return None

def get_host_with_slash(host: str):
  return host if host.endswith("/") else host + "/"
