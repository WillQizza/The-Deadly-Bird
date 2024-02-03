from django.db import models

# Create your models here.
class Node(models.Model):
  id = models.AutoField(primary_key=True)
  host = models.URLField(blank=False, null=False)
  password = models.CharField(max_length=255, blank=False, null=False)