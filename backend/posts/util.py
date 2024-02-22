from following.models import Following
from identity.models import InboxMessage

def send_post_to_inboxes(post_id: int, author_id: int):
  
  followers = Following.objects.filter(target_author=author_id)
  for follower in followers:
    InboxMessage.objects.create(
      author=follower.author,
      content_id=post_id,
      content_type=InboxMessage.ContentType.POST
    )