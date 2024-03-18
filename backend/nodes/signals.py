import requests
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Node
from .util import create_remote_author_if_not_exists

def format_node_api_url(node: Node, route: str):
  if node.host.endswith("/"):
    return node.host[:-1] + route
  else:
    return node.host + route

def create_post_if_not_exists(data: dict[str, any]):
  pass

@receiver(post_save, sender=Node)
def import_public_posts_from_new_node(sender, instance: Node, **kwargs):
  page = 1
  auth = (instance.outgoing_username, instance.outgoing_password)
  
  while True:
    url = format_node_api_url(instance, f"/api/authors/?page={page}")
    print("signal url:", url, "auth: ", auth)
    r = requests.get(url=url, auth=auth)
    if r.status_code != 200:
      # External node error
      print(f"An exception occurred while attempting to fetch authors from {instance.host} (status code = {r.status_code})")
      return
    page += 1

    try:
      members = r.json()["items"]
    except (KeyError, json.JSONDecodeError):
      print(f"{instance.host} does not return the API standardized pagination format.")
      return
    
    if len(members) == 0:
      break
    
    for member in members:
      # Create author in our system if not already created
      create_remote_author_if_not_exists(member)

      # Retrieve all of their posts (both friends and public)
      # TODO: fetch_all_posts()