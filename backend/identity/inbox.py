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
from deadlybird.util import resolve_remote_route, get_host_from_api_url, generate_next_id, remove_trailing_slash
from nodes.util import get_auth_from_host, get_or_create_remote_author_from_api_payload
from posts.models import Post, Comment
from likes.models import Like
from posts.serializers import InboxPostSerializer, InboxCommentSerializer
from deadlybird.util import resolve_remote_route, get_host_with_slash, compare_domains
from nodes.util import get_or_create_remote_author_from_api_payload

def handle_follow_inbox(request: HttpRequest):
    """
    scenario 1) to_author is on a remote node.
        - use python requests to forward payload.

    scenario 2) to_author is on a local node.
        - save inbox message Object locally.
    """  
    to_author = InboxAuthorSerializer(data=request.data.get('object'))
    from_author = InboxAuthorSerializer(data=request.data.get('actor'))
    print(f"CHECKING IF VALID {to_author.is_valid()} {from_author.is_valid()}")
    if not to_author.is_valid() or not from_author.is_valid():
      return Response({
        "error": True,
        "message": "Author payloads not valid"
      }, status=404)
    
    print(f"checking target author exists")
    if not check_authors_exist(to_author.validated_data["id"]):
      return Response({
        "error": True, "message": "Target author provided does not exist"
      }, status=404)

    print(f"Checking from author exists")
    if not check_authors_exist(from_author.validated_data["id"]):
      remote_author = get_or_create_remote_author_from_api_payload(from_author) 
      if not remote_author:
        return Response({
          "error": True, "message": "Failed to create remote author"
        }, status=400)

    from_author = Author.objects.get(id=from_author.validated_data["id"])
    to_author = Author.objects.get(id=to_author.validated_data["id"])

    print("Checking for existing following...")
    existing_following = Following.objects.filter(author__id=from_author.id, target_author__id=to_author.id).first()
    if existing_following is not None:
        print("from author:", from_author.id)
        print("to author:", to_author.id)

        # If this occurs, then that means that the user unfollowed us and we didn't register it.
        existing_following.delete()
        
    elif FollowingRequest.objects.filter(author__id=from_author.id,  
        target_author__id=to_author.id).exists():
            print("REQUEST 409 from author:", from_author.id)
            print("to author:", to_author.id)
            return Response({
                "error": True,
                "message": "Conflict: Outstanding request in existence"
            }, status=409) 
    try:
      receiving_host = to_author.host
      if not compare_domains(SITE_HOST_URL, receiving_host):
        print("Follow request being sent to remote domain")
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

          print(f"request status = {res.status_code} with text {res.text}")
          if res.ok:
            # create local following request to synrchonize
            follow_req = FollowingRequest.objects.create(
              target_author_id=to_author.id,
              author_id=from_author.id
            )
            print("Successfully sent remote follow request")
            return Response( "error": False, "message": "Successfuly sent remote follow request" }, status=201)
          else:
            return Response({"error": True, "message": "Remote follow request failed"}, status=res.status_code)
        else:
           return Response({ "error": True, "message": "Failed to retrieve authentication and form url" }, status=500) 

      else:
        print("Follow request being sent to local author")
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

def handle_unfollow_inbox(request: HttpRequest):
  print("Unfollow Detected")
  to_author = InboxAuthorSerializer(data=request.data.get('object'))
  from_author = InboxAuthorSerializer(data=request.data.get('actor'))
  print(f"Valid Check: {to_author.is_valid()} {from_author.is_valid()}")
  if not to_author.is_valid() or not from_author.is_valid():
    return Response({
      "error": True,
      "message": "Author payloads not valid"
    }, status=404)

  # delete follow object
  obj = Following.objects.filter(author_id=from_author.validated_data["id"], target_author_id=to_author.validated_data["id"]).first()
  if obj:
    print("Deleting follow object...")
    obj.delete()

  return Response("Successfuly unfollwed", status=204) 

def handle_follow_response_inbox(request: HttpRequest):
  print("Got Follow Response")
  to_author = InboxAuthorSerializer(data=request.data.get('object'))
  from_author = InboxAuthorSerializer(data=request.data.get('actor'))

  print(f"Checking FollowResponse authors {to_author.is_valid()} {from_author.is_valid()}")
  if not to_author.is_valid() or not from_author.is_valid():
    return Response({
      "error": True,
      "message": "Author payloads not valid"
    }, status=404)

  print("checking approval")
  if request.data.get('accepted'):
    print(f"accepted. Creating following... {to_author.validated_data['id']} and {from_author.validated_data['id']}")
    Following.objects.get_or_create(
        author_id=to_author.validated_data["id"],
        target_author_id=from_author.validated_data["id"],
    )

  print("Deleting follow request")
  # delete follow request
  follow_req = FollowingRequest.objects.filter(
      author_id=to_author.validated_data["id"], 
      target_author_id=from_author.validated_data["id"],
  ).first()
  if follow_req:
    print("Found follow request to delete.")
    inbox_msg = InboxMessage.objects.filter(content_id=follow_req.id).first()
    if inbox_msg:
      inbox_msg.delete()
    follow_req.delete()

  return Response("Successfuly created follow", status=201) 
      
def _like_post(request: HttpRequest, post_id, source_author):
  # someone liked a post
  try:
    post = Post.objects.get(id=post_id)
  except Post.DoesNotExist:
    return Response({
      "error": True,
      "message": "Post was not found"
    }, status=404)
  
  if post.origin_post is not None:
    post = post.origin_post
  
  if not compare_domains(post.origin, SITE_HOST_URL):
    # Remote post, forward inbox like to origin
    origin_author_id, _, origin_post_id = post.origin.split("/")[-3:]
    payload = {
      "summary": f"{source_author.display_name} liked your post",
      "type": "Like",
      "author": InboxAuthorSerializer(source_author).data,
      "object": resolve_remote_route(get_host_from_api_url(post.origin), view="post", kwargs={ "author_id": origin_author_id, "post_id": origin_post_id })
    }

    url = resolve_remote_route(get_host_from_api_url(post.origin), "inbox", {
        "author_id": origin_author_id
    })

    auth = get_auth_from_host(get_host_from_api_url(post.origin))
    response = requests.post(
      url=url,
      headers={'Content-Type': 'application/json'}, 
      data=json.dumps(payload), 
      auth=auth
    )

    if not response.ok:
      print(f"An error occurred while propagating a remote post like to \"{url}\" (status={response.status_code})")
    else:
      # Create a local copy of it so that our /liked route works fin

      Like.objects.create(
        send_author=source_author,
        receive_author=post.author,
        content_id=post.id,
        content_type=Like.ContentType.POST
      )

    return Response(response.json(), status=response.status_code)

  # We are the origin, like the post.

  # Check if like already exists
  existing_like = Like.objects.filter(content_type=Like.ContentType.POST, 
                      send_author=source_author, 
                      content_id=post.id).first()
  if existing_like is not None:
    return Response({
      "error": True,
      "message": "Like already exists"
    }, status=409)

  Like.objects.create(
    send_author=source_author,
    receive_author=post.author,
    content_id=post.id,
    content_type=Like.ContentType.POST
  )
  
  return Response({
    "error": False,
    "message": "Liked!"
  }, status=201)

def _like_comment(request: HttpRequest, post_id, comment_id, source_author):
  # someone liked a comment
  try:
    post = Post.objects.get(id=post_id)
  except Post.DoesNotExist:
    return Response({
      "error": True,
      "message": "Post was not found"
    }, status=404)
  
  if post.origin_post is not None:
    post = post.origin_post

  if not compare_domains(post.origin, SITE_HOST_URL):
    # Remote comment, forward inbox like to origin
    origin_author_id, _, origin_post_id = post.origin.split("/")[-3:]
    payload = {
      "summary": f"{source_author.display_name} liked your comment",
      "type": "Like",
      "author": InboxAuthorSerializer(source_author).data,
      "object": f'{resolve_remote_route(get_host_from_api_url(post.origin), view="comments", kwargs={ "author_id": origin_author_id, "post_id": origin_post_id })}/{comment_id}'
    }

    url = resolve_remote_route(get_host_from_api_url(post.origin), "inbox", {
        "author_id": origin_author_id
    })

    auth = get_auth_from_host(get_host_from_api_url(post.origin))
    response = requests.post(
      url=url,
      headers={'Content-Type': 'application/json'}, 
      data=json.dumps(payload), 
      auth=auth
    )

    if not response.ok:
      print(f"An error occurred while propagating a remote comment like to \"{url}\" (status={response.status_code})")
    else:
      # Create a local copy of it so that our /liked route works fine
      Like.objects.create(
        send_author=source_author,
        receive_author=post.author,
        content_id=comment_id,
        content_type=Like.ContentType.COMMENT
      )

    return Response(response.json(), status=response.status_code)

  # We are the origin, like the comment.
  try:
    comment = Comment.objects.get(id=comment_id, post=post)
  except Comment.DoesNotExist:
    return Response({
      "error": True,
      "message": "Comment was not found"
    }, status=404)
  
  # Check if like already exists
  existing_like = Like.objects.filter(content_type=Like.ContentType.COMMENT, 
                      send_author=source_author, 
                      content_id=comment.id).first()
  if existing_like is not None:
    return Response({
      "error": True,
      "message": "Like already exists"
    }, status=409)

  Like.objects.create(
      send_author=source_author,
      receive_author=comment.author,
      content_id=comment.id,
      content_type=Like.ContentType.COMMENT
  )
  
  return Response({
    "error": False,
    "message": "Liked!"
  }, status=201)

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
  
  like_object = remove_trailing_slash(like_object)
  
  # Ensure the author sending the like exists
  # In the case the author does not exist within our system, it's a remote author who's liking it.
  author_who_created_like = get_or_create_remote_author_from_api_payload(author_payload)
  
  like_type, id = like_object.split("/")[-2:]
  like_type = Like.ContentType.POST if like_type.lower() == "posts" else Like.ContentType.COMMENT

  if like_type == Like.ContentType.POST:
    return _like_post(request, post_id=id, source_author=author_who_created_like)
  else:
    post_id = like_object.split("/")[-3]
    return _like_comment(request, post_id=post_id, comment_id=id, source_author=author_who_created_like)

def handle_post_inbox(request: HttpRequest, target_author_id: str):
  """
  This will only be called when a remote node is sending us a post
  """
  serializer = InboxPostSerializer(data=request.data)
  if not serializer.is_valid():
    return Response({ "error": True, "message": "Invalid post payload" }, status=400)
  
  print("received post inbox message")
  print(serializer.data)

  # Ensure the origin author exists in our systems
  origin_url = serializer.data["origin"]
  origin_author_id = origin_url.split("/")[-3]
  try:
    origin_author = Author.objects.get(id=origin_author_id)
  except Author.DoesNotExist:
    # Source author does not exist in our systems. Register them
    origin_host = get_host_from_api_url(origin_url)
    url = resolve_remote_route(origin_host, "author", {
      "author_id": origin_author_id
    })
    auth = get_auth_from_host(origin_host)    
    res = requests.get(
      url=url,
      auth=auth
    )
    
    if not res.ok:
      print(f"Failed to get origin author from \"{url}\" using credentials.")
      return Response({ "error": True, "message": "Failed to GET origin author" }, status=500)

    origin_author_serializer = InboxAuthorSerializer(data=res.json())
    if not origin_author_serializer.is_valid():
      print(f"Failed to parse origin author JSON from \"{url}\"")
      return Response({ "error": True, "message": "Invalid origin author JSON format" }, status=500)
    
    origin_author = get_or_create_remote_author_from_api_payload(origin_author_serializer["data"])

  # Ensure source author also exists in our system
  source_url = serializer.data["source"]
  source_author = get_or_create_remote_author_from_api_payload(serializer.data["author"])

  # Get origin post
  origin_post_id = origin_url.split("/")[-1]
  origin_post = Post.objects.filter(id=origin_post_id).first()

  if source_url == origin_url:

    if origin_post != None:
      # We are sharing a post that we wrote.
      created_post = Post.objects.create(
        origin_post=origin_post,
        origin_author=origin_author,
        title=origin_post.title,
        source=source_url,
        origin=origin_url,
        description=origin_post.description,
        content_type=origin_post.content_type,
        content=origin_post.content,
        author=source_author,
        visibility=Post.Visibility.PUBLIC
      )
    else:
      # Does author match origin author?
      author_and_origin_author_match = origin_author_id == source_author.id

      if author_and_origin_author_match:
        # Create NEW post
        created_post = Post.objects.create(
          id=origin_post_id,
          title=serializer.data["title"],
          source=source_url,
          origin=origin_url,
          description=serializer.data["description"],
          content_type=serializer.data["contentType"],
          content=serializer.data["content"],
          author=source_author,
          visibility=serializer.data["visibility"]
        )
      else:
        # Create origin post from origin url and then create our shared post
        origin_post = Post.objects.create(
          id=origin_post_id,
          title=serializer.data["title"],
          source=source_url,
          origin=origin_url,
          description=serializer.data["description"],
          content_type=serializer.data["contentType"],
          content=serializer.data["content"],
          author=origin_author,
          visibility=serializer.data["visibility"]
        )

        created_post = Post.objects.create(
          origin_post=origin_post,
          origin_author=origin_author,
          title=origin_post.title,
          source=source_url,
          origin=origin_url,
          description=origin_post.description,
          content_type=origin_post.content_type,
          content=origin_post.content,
          author=source_author,
          visibility=Post.Visibility.PUBLIC
        )

  else:
    # We're sharing a post. 

    # Create origin post.
    if origin_post is None:
      origin_post = Post.objects.create(
        id=origin_post_id,
        title=serializer.data["title"],
        source=source_url,
        origin=origin_url,
        description=serializer.data["description"],
        content_type=serializer.data["contentType"],
        content=serializer.data["content"],
        author=origin_author,
        visibility=serializer.data["visibility"]
      )

    # Creat shared post.
    created_post = Post.objects.create(
      origin_post=origin_post,
      origin_author=origin_author,
      title=origin_post.title,
      source=source_url,
      origin=origin_url,
      description=origin_post.description,
      content_type=origin_post.content_type,
      content=origin_post.content,
      author=source_author,
      visibility=Post.Visibility.PUBLIC
    )

  target_author = Author.objects.get(id=target_author_id)
  inbox_post_id = created_post.id if created_post.origin_post is None else created_post.origin_post.id

  # Create inbox message
  InboxMessage.objects.create(
    author=target_author,
    content_id=inbox_post_id,
    content_type=InboxMessage.ContentType.POST
  )

  return Response({
    "error": False,
    "message": "Success"
  }, status=201)

def handle_comment_inbox(request: HttpRequest):
  serializer = InboxCommentSerializer(data=request.data)
  if not serializer.is_valid():
    return Response({
      "error": True,
      "message": "Invalid comment payload."
    }, status=400)
  
  post_id, arg, comment_id = serializer.data["id"].split("/")[-3:]
  
  # Temporary hack in case scenario of /posts/id instead of /posts/id/comments/id 
  if arg.lower() == "posts":
    post_id = comment_id
    comment_id = generate_next_id()
    
  post = Post.objects.get(id=post_id)

  if post.origin_post != None:
    # This is a shared post!
    post = post.origin_post

  if not compare_domains(post.origin, SITE_HOST_URL):
    # Remote post. Redirect to proper remote host
    url = resolve_remote_route(post.author.host, "inbox", {
        "author_id": post.author.id
    })
    auth = get_auth_from_host(post.author.host)

    payload = {
      "type": serializer.data["type"],
      "id": f'{resolve_remote_route(post.author.host, "comments", kwargs={ "author_id": post.author.id, "post_id": post.id })}/{comment_id}',
      "author": serializer.data["author"],
      "comment": serializer.data["comment"],
      "contentType": serializer.data["contentType"],
      "published": serializer.data["published"]
    }

    response = requests.post(
      url=url,
      headers={'Content-Type': 'application/json'}, 
      data=json.dumps(payload), 
      auth=auth
    )
    return Response(response.json(), status=response.status_code)
    

  author = get_or_create_remote_author_from_api_payload(serializer.data["author"])
  comment = Comment.objects.create(
    id=comment_id,
    post=post,
    author=author,
    content_type=serializer.data["contentType"],
    content=serializer.data["comment"]
  )

  InboxMessage.objects.create(
    author=post.author,
    content_id=comment.id,
    content_type=InboxMessage.ContentType.COMMENT
  )

  return Response({
    "error": False,
    "message": "Success"
  })
