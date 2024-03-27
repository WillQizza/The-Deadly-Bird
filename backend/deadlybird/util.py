from django.urls import reverse
from django.conf import settings
from deadlybird.settings import SITE_HOST_URL
from urllib.parse import urljoin, urlparse
import os
import uuid

def generate_next_id():
  return str(uuid.uuid4())

def generate_full_api_url(view: str, force_no_slash = False, kwargs: dict[str, str] = None):
  if settings.SITE_HOST_URL.endswith("/"):
    api_url = settings.SITE_HOST_URL + reverse(view, kwargs=kwargs)[1:]
  else:
    api_url = settings.SITE_HOST_URL + reverse(view, kwargs=kwargs)
  
  if force_no_slash and api_url.endswith("/"):
    api_url = api_url[:-1]
  
  return dockerize_localhost(api_url)

def resolve_remote_route(host: str, view: str, kwargs = None, args = None, force_no_slash = False):
  """
  Given the hostname of an author, we may have to swap the hostname to escape
  the dockercontainer and construct a url to the host. Only applicable to local dev.
  """    
  route = reverse(viewname=view, kwargs=kwargs, args=args)
  url = urljoin(dockerize_localhost(host), route)

  if url.endswith("/") and force_no_slash:
    return url[:-1]
  else:
    return url

def dockerize_localhost(host: str):
  """
  We need to replace localhost with host.docker.internal or else it will redirect
  requests to the internal container network rather than the host network.
  """
  if os.environ.get("DOCKER") is not None:
    host = host.replace("localhost", "host.docker.internal")
    
  return host

def resolve_docker_host(host: str):
  """
  We need to undo resolve_remote_route if trying to filter authors that
  match a host field of a node instance.
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

def normalize_author_host(host: str):
  pasrsed_url = urlparse(host)
  #             http or https         host + port if exists
  hostname = f"{pasrsed_url.scheme}://{pasrsed_url.netloc}"

  return hostname

def compare_domains(url1, url2):
    """
    Compares the domain and port of two URLs to determine if they are equal.
    """
    parsed_url_1 = urlparse(url1)
    parsed_url_2 = urlparse(url2)

    domain1, port1 = (dockerize_localhost(parsed_url_1.hostname), parsed_url_1.port)
    domain2, port2 = (dockerize_localhost(parsed_url_2.hostname), parsed_url_2.port) 

    if port1 and port2:
      return domain1 == domain2 and port1 == port2
    else: 
      return domain1 == domain2