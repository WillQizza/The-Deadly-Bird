from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post, Comment
from identity.models import InboxMessage
from likes.models import Like

@receiver(post_delete, sender=Post)
def handle_delete_post(sender, instance: Post, **kwargs):
  post_id = instance.id
  Like.objects.all().filter(content_type=Like.ContentType.POST, content_id=post_id).delete()
  InboxMessage.objects.all().filter(content_type=InboxMessage.ContentType.POST, content_id=post_id).delete()

@receiver(post_delete, sender=Comment)
def handle_delete_comment(sender, instance: Comment, **kwargs):
  comment_id = instance.id
  Like.objects.all().filter(content_type=Like.ContentType.COMMENT, content_id=comment_id).delete()
  InboxMessage.objects.all().filter(content_type=InboxMessage.ContentType.COMMENT, content_id=comment_id).delete()
