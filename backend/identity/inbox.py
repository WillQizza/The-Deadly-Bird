# Utility file to factor out the large inbox view in views.py
import requests
from django.http import HttpRequest
from rest_framework.response import Response
from .models import Author, InboxMessage
from following.models import Following, FollowingRequest 
from identity.util import check_authors_exist
from deadlybird.settings import SITE_HOST_URL
from nodes.util import get_auth_from_host
from posts.models import Post, Comment
from likes.models import Like
import json
from deadlybird.util import resolve_remote_route
  

def handle_follow_inbox(request: HttpRequest):
    """
    scenario 1) to_author is on a remote node.
        - use python requests to forward payload.

    scenario 2) to_author is on a local node.
        - save inbox message Object locally.
    """  
    to_author = request.data.get('object')
    from_author = request.data.get('actor')
    
    if not check_authors_exist(to_author["id"], from_author["id"]):
      return Response({
        "error": True,
        "message": "An author provided does not exist"
      }, status=404)

    from_author = Author.objects.get(id=from_author["id"])
    to_author = Author.objects.get(id=to_author["id"])

    if Following.objects.filter(author__id=from_author.id,
                                target_author__id=to_author.id).exists(): 
        return Response({
            "error": True,
            "message": "Conflict: Author is already following"
        }, status=409)
    elif FollowingRequest.objects.filter(author__id=from_author.id, 
        target_author__id=to_author.id).exists():
            return Response({
                "error": True,
                "message": "Conflict: Outstanding request in existence"
            }, status=409) 
    try:
      receiving_host = to_author.host
      if SITE_HOST_URL not in receiving_host:
        # Remote Following Request

        url = resolve_remote_route(receiving_host, "inbox", {
           "author_id": to_author.id
        })

        auth = get_auth_from_host(receiving_host)
        if auth is not None and url is not None: 
          print("auth: ", auth, "url: ", url, "data:", json.dumps(request.data))
          res = requests.post(
            url=url,
            headers={'Content-Type': 'application/json'}, 
            data=json.dumps(request.data), 
            auth=auth
          )
          if res.status_code == 201:
            return Response("Successfuly sent remote follow request", status=201) 
          else:
            return Response({"error": True, "message": "Remote post Failed"}, status=res.status_code)
        else:
           return Response("Failed to retrieve authentication and form url", status=500) 

      else:
        # Local Following Request
        follow_req = FollowingRequest.objects.create(
            target_author_id=to_author.id,
            author_id=from_author.id
        )
        InboxMessage.objects.create(
            author_id=to_author.id,
            content_id=follow_req.id,
            content_type=InboxMessage.ContentType.FOLLOW
        ) 
      return Response({
        "error": False,
        "message": "Successfuly created follow request and inbox message."
      }, status=201)   
    except:
      return Response({
          "error": True,
          "message": "Failed to create FollowRequest or InboxMessage"
      }, status=500) 
      
def handle_like_inbox(request: HttpRequest):
  """
  This will only be called when a local node likes a post/comment or a remote node liked one of our posts/comments
  """
  author_payload = request.data.get("author")
  like_object = request.data.get("object")

  # Ensure data exists
  if (author_payload is None) or (like_object is None) or not ("id" in author_payload):
    return Response({
      "error": True,
      "message": "Incomplete like payload"
    }, status=400)
  
  like_type, id = like_object.split("/")[-2:]
  like_type = Like.ContentType.POST if like_type.lower() == "posts" else Like.ContentType.COMMENT

  try:
    source = Post.objects.get(id=id) if like_type == Like.ContentType.POST else Comment.objects.get(id=id)

    # Special case in the scenario we are liking a shared post
    if like_type == Like.ContentType.POST and source.origin_post != None:
      source = source.origin_post
  except (Post.DoesNotExist, Comment.DoesNotExist):
    return Response({
      "error": True,
      "message": "Object does not exist"
    }, status=404)
  
  # Check if like already exists
  existing_like = Like.objects.filter(content_type=like_type, 
                      send_author=author_payload["id"], 
                      content_id=source.id).first()
  
  if existing_like is not None:
    return Response({
      "error": True,
      "message": "Like already exists"
    }, status=409)
  
  like = Like.objects.create(
      send_author_id=author_payload["id"],
      receive_author_id=source.author.id,
      content_id=source.id,
      content_type=like_type
  )
  content_id = like.id

  # Create inbox message
  InboxMessage.objects.create(
    author=source.author,
    content_id=content_id,
    content_type=InboxMessage.ContentType.LIKE
  )

  return Response({ "error": False, "message": "Success" })

def handle_post_inbox(request: HttpRequest):
  """
  This will only be called when a remote node is sending us a post
  """
  