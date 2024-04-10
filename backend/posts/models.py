from django.db import models
from identity.models import Author
from following.models import Following
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

  id = models.CharField(primary_key=True, max_length=255, default=generate_next_id)
  # Original post object (used only when sharing posts)
  title = models.CharField(max_length=255, blank=False, null=False)
  source = models.URLField(blank=False, null=False)
  origin = models.URLField(blank=False, null=False)
  origin_author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True, related_name="post_origin_author")
  description = models.CharField(max_length=255, blank=False, null=False)
  content_type = models.CharField(choices=ContentType.choices, max_length=30, blank=False, null=False)
  content = models.TextField(blank=False, null=False)
  author = models.ForeignKey(Author, blank=False, null=False, on_delete=models.CASCADE)
  published_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
  visibility = models.CharField(choices=Visibility.choices, max_length=8, blank=False, null=False)

  def __str__(self) -> str:
    return f"Post {self.id} - ({self.author.display_name}) [{self.content_type}] [{self.visibility}]"

class Comment(models.Model):
  class ContentType(models.TextChoices):
    MARKDOWN = "text/markdown"
    PLAIN = "text/plain"
    
  id = models.CharField(primary_key=True, max_length=255, default=generate_next_id)
  post = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE)
  author = models.ForeignKey(Author, blank=False, null=False, on_delete=models.CASCADE)
  content_type = models.CharField(choices=ContentType.choices, max_length=30, blank=False, null=False)
  content = models.TextField(blank=False, null=False)
  published_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)

class FollowingFeedPost(models.Model):
  id = models.CharField(primary_key=True, max_length=255, default=generate_next_id)
  post = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE)
  follower = models.ForeignKey(Author, blank=False, null=False, on_delete=models.CASCADE, related_name="feed_follower")
  from_author = models.ForeignKey(Author, blank=False, null=False, on_delete=models.CASCADE, related_name="feed_from_author")
  published_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)