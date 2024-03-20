# Utility file to factor out the large inbox view in views.py
import requests
import json
from django.http import HttpRequest
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Author, InboxMessage
from following.models import Following, FollowingRequest 
from identity.util import check_authors_exist
from identity.serializers import InboxAuthorSerializer
from deadlybird.settings import SITE_HOST_URL
from deadlybird.util import resolve_remote_route, get_host_from_api_url
from nodes.util import get_auth_from_host, create_remote_author_if_not_exists
from posts.models import Post, Comment
from likes.models import Like
from posts.serializers import InboxPostSerializer
from deadlybird.util import resolve_remote_route, get_host_with_slash
  

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
            # create local following request to synrchonize
            follow_req = FollowingRequest.objects.create(
              target_author_id=to_author.id,
              author_id=from_author.id
            )
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
  
  # Ensure the author sending the like exists
  # In the case the author does not exist within our system, it's a remote author who's liking it.
  author_who_created_like = create_remote_author_if_not_exists(author_payload)
  
  like_type, id = like_object.split("/")[-2:]
  like_type = Like.ContentType.POST if like_type.lower() == "posts" else Like.ContentType.COMMENT

  try:
    content_source = Post.objects.get(id=id) if like_type == Like.ContentType.POST else Comment.objects.get(id=id)

    # Special case in the scenario we are liking a locally shared post
    if like_type == Like.ContentType.POST and content_source.origin_post != None:
      content_source = content_source.origin_post

    if like_type == Like.ContentType.POST and (SITE_HOST_URL not in content_source.source):
      # TODO: DO LATER AFTER TALKING TO HAZEL ABOUT HOW REMOTE LIKES OM COMMENTS WORK
      # We are liking a post that did not originate from this node, so forward the inbox there instead.
      payload = {
        "summary": request.data.get("summary"),
        "type": "Like",
        "author": InboxAuthorSerializer(author_who_created_like).data,
        "object": content_source.source
      }

      url = resolve_remote_route(content_source.author.host, "inbox", {
          "author_id": content_source.author.id
      })

      auth = get_auth_from_host(content_source.author.host)
      response = requests.post(
        url=url,
        headers={'Content-Type': 'application/json'}, 
        data=json.dumps(payload), 
        auth=auth
      )

      if not response.ok:
        print(f"An error occurred while propagating a remote like to \"{url}\" (status={response.status_code})")

      return Response(response.json(), status=response.status_code)

    if like_type == Like.ContentType.COMMENT and (SITE_HOST_URL not in content_source.post.author.host):
      # TODO: DO LATER AFTER TALKING TO HAZEL ABOUT HOW REMOTE LIKES OM COMMENTS WORK
      # We are liking a comment whose post does does not originate from this node, so forward the like there instead.
      comment_object = f"{get_host_with_slash(content_source.post.author.host)}api/authors/{content_source.post.author.id}/posts/{content_source.post.id}/comments/{content_source.id}"

      payload = {
        "summary": request.data.get("summary"),
        "type": "Like",
        "author": InboxAuthorSerializer(author_who_created_like).data,
        "object": comment_object
      }

      # TODO: Consider if author was shared post author

      url = resolve_remote_route(content_source.post.author.host, "inbox", {
          "author_id": content_source.author.id
      })

      auth = get_auth_from_host(content_source.post.author.host)
      response = requests.post(
        url=url,
        headers={'Content-Type': 'application/json'}, 
        data=json.dumps(payload), 
        auth=auth
      )

      if not response.ok:
        print(f"An error occurred while propagating a remote like to \"{url}\" (status={response.status_code})")
      
      return Response(response.json(), status=response.status_code)
  except (Post.DoesNotExist, Comment.DoesNotExist):
    return Response({
      "error": True,
      "message": "Object does not exist"
    }, status=404)
  
  # We are the node who houses the post/comment we are liking
  
  # Check if like already exists
  existing_like = Like.objects.filter(content_type=like_type, 
                      send_author=author_payload["id"], 
                      content_id=content_source.id).first()
  
  if existing_like is not None:
    return Response({
      "error": True,
      "message": "Like already exists"
    }, status=409)
  
  like = Like.objects.create(
      send_author_id=author_payload["id"],
      receive_author_id=content_source.author.id,
      content_id=content_source.id,
      content_type=like_type
  )
  content_id = like.id

  # Create inbox message
  InboxMessage.objects.create(
    author=content_source.author,
    content_id=content_id,
    content_type=InboxMessage.ContentType.LIKE
  )

  return Response({ "error": False, "message": "Success" }, status=201)

def handle_post_inbox(request: HttpRequest, target_author_id: str):
  """
  This will only be called when a remote node is sending us a post
  """
  serializer = InboxPostSerializer(data=request.data)
  if not serializer.is_valid():
    return Response({ "error": True, "message": "Invalid post payload" }, status=400)

  # Create the remote author if they do not exist in our system (origin author)
  author_data = serializer.data["author"]
  origin_author = create_remote_author_if_not_exists(author_data)

  origin_url = serializer.data["origin"]
  origin_post_id = origin_url.split("/")[-1]

  # Ensure the source author also exists in our systems
  source_url = serializer.data["source"]
  source_author_id = source_url.split("/")[-3]
  try:
    source_author = Author.objects.get(id=source_author_id)
  except Author.DoesNotExist:
    # Source author does not exist in our systems. Register them
    source_host = get_host_from_api_url(source_url)
    url = resolve_remote_route(source_host, "author", {
      "author_id": source_author_id
    })
    auth = get_auth_from_host(source_host)    
    res = requests.get(
      url=url,
      auth=auth
    )
    
    if not res.ok:
      print(f"Failed to get source author from \"{url}\" using credentials.")
      return Response({ "error": True, "message": "Failed to GET source author" }, status=500)

    source_author_serializer = InboxAuthorSerializer(data=res.json())
    if not source_author_serializer.is_valid():
      print(f"Failed to parse source author JSON from \"{url}\"")
      return Response({ "error": True, "message": "Invalid source author JSON format" }, status=500)
    
    source_author = create_remote_author_if_not_exists(source_author_serializer["data"])

  # We now have origin_author and source_author

  is_normal_post_propagation = origin_post_id == serializer.data["id"]

  if is_normal_post_propagation:
    # Normal post propagation, just create the post if it does not exist in our system
    try:
      post = Post.objects.get(id=serializer.data["id"])
    except Post.DoesNotExist:
      post = Post.objects.create(
        id=serializer.data["id"],
        title=serializer.data["title"],
        source=serializer.data["source"],
        origin=serializer.data["origin"],
        description=serializer.data["description"],
        content_type=serializer.data["contentType"],
        content=serializer.data["content"],
        author=origin_author,
        published_date=serializer.data["published"],
        visibility=serializer.data["visibility"]
      )
  else:
    # Post propagation of a shared post
    # Ensure origin post exists
    try:
      origin_post = Post.objects.get(id=origin_post_id)
    except Post.DoesNotExist:
      origin_post = Post.objects.create(
        id=origin_post_id,
        title=serializer.data["title"],
        source=serializer.data["source"],
        origin=serializer.data["origin"],
        description=serializer.data["description"],
        content_type=serializer.data["contentType"],
        content=serializer.data["content"],
        author=origin_author,
        published_date=serializer.data["published"],
        visibility=serializer.data["visibility"]
      )

    # Create shared post if not exist
    try:
      post = Post.objects.get(id=serializer.data["id"])
    except Post.DoesNotExist:
      post = Post.objects.create(
        id=serializer.data["id"],
        title=serializer.data["title"],
        source=serializer.data["source"],
        origin=serializer.data["origin"],
        description=serializer.data["description"],
        content_type=serializer.data["contentType"],
        content=serializer.data["content"],
        author=source_author,
        origin_author=origin_author,
        origin_post=origin_post,
        published_date=serializer.data["published"],
        visibility=serializer.data["visibility"]
      )

  target_author = Author.objects.get(id=target_author_id)

  # Create inbox message
  InboxMessage.objects.create(
    author=target_author,
    content_id=post.id,
    content_type=InboxMessage.ContentType.POST
  )

  return Response({
    "error": False,
    "message": "Success"
  }, status=201)