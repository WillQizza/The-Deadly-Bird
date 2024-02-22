from django.db import models
from identity.models import Author
from nodes.models import Node
from deadlybird.util import generate_next_id

# Create your models here.
class Post(models.Model):
  class ContentType(models.TextChoices):
    MARKDOWN = "text/markdown"
    PLAIN = "text/plain"
    APPLICATION_BASE64 = "application/base64"
    PNG_BASE64 = "image/png;base64"
    JPEG_BASE64 = "image/jpeg;base64"
  class Visibility(models.TextChoices):
    PUBLIC = "PUBLIC"
    FRIENDS = "FRIENDS"
    UNLISTED = "UNLISTED"

  id = models.CharField(primary_key=True, max_length=10, default=generate_next_id)
  title = models.CharField(max_length=255, blank=False, null=False)
  source = models.ForeignKey(Node, blank=True, null=True, on_delete=models.CASCADE)
  origin = models.CharField(max_length=255, blank=True, null=True)
  description = models.CharField(max_length=255, blank=False, null=False)
  content_type = models.CharField(choices=ContentType.choices, max_length=30, blank=False, null=False)
  content = models.TextField(blank=False, null=False)
  author = models.ForeignKey(Author, blank=False, null=False, on_delete=models.CASCADE)
  published_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
  visibility = models.CharField(choices=Visibility.choices, max_length=8, blank=False, null=False)

class Comment(models.Model):
  class ContentType(models.TextChoices):
    MARKDOWN = "text/markdown"
    PLAIN = "text/plain"
    APPLICATION_BASE64 = "application/base64"
    PNG_BASE64 = "image/png;base64"
    JPEG_BASE64 = "image/jpeg;base64"
    
  id = models.CharField(primary_key=True, max_length=10, default=generate_next_id)
  post = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE)
  author = models.ForeignKey(Author, blank=False, null=False, on_delete=models.CASCADE)
  content_type = models.CharField(choices=ContentType.choices, max_length=30, blank=False, null=False)
  content = models.TextField(blank=False, null=False)
  published_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)