from django.db import models
from deadlybird.util import generate_next_id

# Create your models here.
class Node(models.Model):
  id = models.CharField(primary_key=True, max_length=10, default=generate_next_id)
  host = models.URLField(blank=False, null=False)
  password = models.CharField(max_length=255, blank=False, null=False)