from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Author(models.Model):
  id = models.AutoField(primary_key=True)
  user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
  host = models.CharField(max_length=255, blank=False, null=False)
  github = models.CharField(max_length=255, blank=True, null=True)
  bio = models.CharField(max_length=255, blank=True, null=False, default="")
  profile_url = models.CharField(max_length=255, blank=False, null=False)
  profile_picture = models.CharField(max_length=255, blank=True, null=True)

class InboxMessage(models.Model):
  class ContentType(models.TextChoices):
    POST="post"
    FOLLOW="follow"
    LIKE="like"
    COMMENT="comment"

  id = models.AutoField(primary_key=True)
  author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=False, null=False)
  content_id = models.IntegerField(blank=False, null=False)
  content_type = models.CharField(choices=ContentType.choices, max_length=50, blank=False, null=False)