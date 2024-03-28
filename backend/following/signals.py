from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import FollowingRequest
from identity.models import InboxMessage

@receiver(post_delete, sender=FollowingRequest)
def handle_delete_follow_request(sender, instance: FollowingRequest, **kwargs):
  follow_request_id = instance.id
  InboxMessage.objects.all().filter(content_type=InboxMessage.ContentType.FOLLOW, content_id=follow_request_id).delete()