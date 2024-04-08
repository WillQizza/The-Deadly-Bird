from following.models import Following
from following.util import is_friends
from identity.models import InboxMessage, Author
from deadlybird.settings import SITE_HOST_URL
from nodes.util import get_auth_from_host
from deadlybird.util import resolve_remote_route, generate_full_api_url, compare_domains
from .serializers import InboxPostSerializer
from .models import Post, FollowingFeedPost
import requests
import json

def send_post_to_inboxes(post_id: str, author_id: str):
  post = Post.objects.get(id=post_id)
  if post.visibility == Post.Visibility.UNLISTED:
    return  # Unlisted posts do not get sent to inboxes

  followers = Following.objects.filter(target_author=author_id)
  for follower in followers:
    if post.visibility == Post.Visibility.FRIENDS and not is_friends(author_id, follower.author.id):
      continue  # Friend posts should only be sent to the inboxes of friends

    if not compare_domains(follower.author.host, SITE_HOST_URL):
      print(f"PUBLISHING MESSAGE FROM {author_id} OF {post_id} TO {follower.author.id}")
      # Remote follower, we have to publish the post to their inbox
      url = resolve_remote_route(follower.author.host, "inbox", {
          "author_id": follower.author.id
      })
      auth = get_auth_from_host(follower.author.host)

      if post.author.id != author_id:
        # This is a shared post, we need to update the author of the post
        post.author = Author.objects.get(id=author_id)
        post.source = generate_full_api_url("post", kwargs={ "author_id": author_id, "post_id": post.id })

      payload = InboxPostSerializer(post).data
      response = requests.post(
        url=url,
        headers={'Content-Type': 'application/json'}, 
        data=json.dumps(payload), 
        auth=auth
      )

      if not response.ok:
        print(f"Failed to send inbox message {post_id} to {url}")
        print(response.text)

    else:
      # Local follower, so we can just publish the inbox message and be done 
      InboxMessage.objects.create(
        author=follower.author,
        content_id=post_id,
        content_type=InboxMessage.ContentType.POST
      )
      FollowingFeedPost.objects.create(
        post=post,
        follower=follower,
        from_author_id=author_id
      )