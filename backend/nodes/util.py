from .models import Node
from identity.models import Author
from django.contrib.auth.models import User
from deadlybird.util import generate_next_id, normalize_author_host, compare_domains
from django.db.utils import IntegrityError
from django.utils import timezone
from identity.serializers import InboxAuthorSerializer
import json

def format_node_api_url(node: Node, route: str):
  if node.host.endswith("/"):
    return node.host[:-1] + route
  else:
    return node.host + route

def get_auth_from_host(host: str):
    "Given host return the authentication tuple"

    nodes = Node.objects.all()
    for node in nodes:
       if compare_domains(node.host, host):
          return (node.outgoing_username, node.outgoing_password)
       
    print(f"Could not find credentials to requested host: {host} - Using default credentials")
    return ('username', 'password')

def get_or_create_remote_author_from_api_payload(data: dict[str, any]):
  serializer = InboxAuthorSerializer(data=data)
  if not serializer.is_valid():
    print(f"Unable to parse remote author JSON: {json.dumps(data)}")
    print(serializer.errors)
    return None
  data = serializer.validated_data
  
  try:
    author = Author.objects.get(id=data["id"])
    if author.profile_picture != data["profile_picture"]:
      author.profile_picture = data["profile_picture"]
      author.save()
    if author.github != data["github"]:
      author.github = data["github"]
      author.save()
    if author.display_name != data["display_name"]:
      author.display_name = data["display_name"]
      author.save()

    return author
  except Author.DoesNotExist:
   
    try: 
      created_user = User.objects.create_user(
        # TODO: RETHINK THIS OUT LATER: 
        # Problem is what if two nodes have an author with the same username?
        username=data["display_name"] + "-" + generate_next_id()[0:7],
        email=None,
        password=None,
      )
      created_user.is_active = False    # Remote users should not be allowed to login
      created_user.save()

      # Create author object from user object
      print("Creating user")
      print(data)
      return Author.objects.create(
        id=data["id"], #same id as remote object          
        user=created_user,
        display_name=data["display_name"],
        host=normalize_author_host(data["host"]),
        profile_url=data["profile_url"],
        profile_picture=data["profile_picture"],
        last_github_check=timezone.now(),
        github=data["github"]
      )

    except IntegrityError as e:
      print("integrity error")
      print(e)