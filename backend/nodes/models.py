import secrets
from django.db import models
from deadlybird.util import generate_next_id

def generate_random_credential():
  return secrets.token_urlsafe(16)

# Create your models here.
class Node(models.Model):
  id = models.CharField(primary_key=True, max_length=255, default=generate_next_id)
  host = models.URLField(blank=False, null=False)
  outgoing_username = models.CharField(max_length=255, blank=False, null=False)
  outgoing_password = models.CharField(max_length=255, blank=False, null=False)
  
  def __str__(self):
    return f"Node ({self.host})"