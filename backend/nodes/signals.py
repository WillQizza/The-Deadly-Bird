import requests
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Node
from identity.models import Author
from django.contrib.auth.models import User

def format_node_api_url(node: Node, route: str):
  if node.host.endswith("/"):
    return node.host[:-1] + route
  else:
    return node.host + route
  
def create_author_if_not_exists(data: dict[str, any]):
  try:
    Author.objects.get(id=data["id"])
  except Author.DoesNotExist:
    # TODO: RETHINK THIS OUT LATER: Problem is what if two nodes have an author with the same username?
    User.objects.create(

    )
    Author.objects.create(

    )

def create_post_if_not_exists(data: dict[str, any]):
  pass

@receiver(post_save, sender=Node)
def import_public_posts_from_new_node(sender, instance: Node, **kwargs):
  page = 1
  auth = (instance.outgoing_username, instance.outgoing_username)
  
  while True:
    r = requests.get(format_node_api_url(instance, f"/authors/?page={page}"), auth=auth)
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
      create_author_if_not_exists(member)

      # Retrieve all of their posts (both friends and public)
      fetch_all_posts()