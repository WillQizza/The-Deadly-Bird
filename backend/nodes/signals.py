import requests
import json
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Node
from identity.models import Author
from .util import get_or_create_remote_author_from_api_payload, format_node_api_url
from deadlybird.util import resolve_docker_host, compare_domains

@receiver(post_delete, sender=Node)
def handle_delete_node(sender, instance: Node, **kwargs):

  resolved_host = resolve_docker_host(instance.host)

  remote_authors = Author.objects.filter(host=resolved_host)

  for author in remote_authors: 
    user = author.user
    user.delete()

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
      author = get_or_create_remote_author_from_api_payload(member)

      # Retrieve all of their posts (both friends and public)
      import_public_posts_from_author(author, instance)