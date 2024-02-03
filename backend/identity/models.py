from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Author(models.Model):
  id = models.AutoField(primary_key=True)
  user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
  host = models.CharField(max_length=255, blank=False, null=False)
  github = models.CharField(max_length=255, blank=True, null=True)
  profile_url = models.CharField(max_length=255, blank=False, null=False)
  profile_picture = models.CharField(max_length=255, blank=True, null=True)

class InboxMessage(models.Model):
  CONTENT_TYPE = [] # TODO: At some point this will need to be updated with things like (0, "like") (1, "post") and whatnot

  id = models.AutoField(primary_key=True)
  author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=False, null=False)
  content_id = models.IntegerField(blank=False, null=False)
  content_type = models.IntegerField(blank=False, null=False, choices=CONTENT_TYPE)