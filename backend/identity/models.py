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