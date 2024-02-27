from django.db import models
from identity.models import Author
from posts.models import Post
from deadlybird.util import generate_next_id

class Like(models.Model): 
  class ContentType(models.TextChoices):
    # Liked objects can be posts and comments.
    POST="post"
    COMMENT="comment"

  id = models.CharField(primary_key=True, max_length=255, default=generate_next_id)
  send_author = models.ForeignKey(Author, related_name='sent_like', blank=False, null=False, on_delete=models.CASCADE)
  receive_author = models.ForeignKey(Author, related_name='received_like', blank=False, null=False, on_delete=models.CASCADE)
  content_id = models.CharField(max_length=255, blank=False, null=False)
  content_type = models.CharField(choices=ContentType.choices, max_length=50, blank=False, null=False) 