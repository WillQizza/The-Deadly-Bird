from django.db import models
from identity.models import Author

# Create your models here.
class Post(models.Model):
  CONTENT_TYPE = [
    (0, "text/markdown"),
    (1, "text/plain"),
    (2, "application/base64"),
    (3, "image/png;base64"),
    (4, "image/jpeg;base64")
  ]
  VISIBILITY = [
    (0, "PUBLIC"),
    (1, "FRIENDS"),
    (2, "UNLISTED")
  ]
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=255, blank=False, null=False)
  source = models.CharField(max_length=255, blank=False, null=False)
  origin = models.CharField(max_length=255, blank=False, null=False)
  description = models.CharField(max_length=255, blank=False, null=False)
  content_type = models.IntegerField(choices=CONTENT_TYPE, blank=False, null=False)
  content = models.TextField(blank=False, null=False)
  author = models.ForeignKey(Author, blank=False, null=False, on_delete=models.CASCADE)
  published_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
  visibility = models.IntegerField(choices=VISIBILITY, blank=False, null=False)

class PostCategoryMeta(models.Model):
  id = models.AutoField(primary_key=True)
  post = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE)
  category = models.CharField(max_length=255, blank=False, null=False)

class Comment(models.Model):
  CONTENT_TYPE = [
    (0, "text/markdown"),
    (1, "text/plain"),
    (2, "application/base64"),
    (3, "image/png;base64"),
    (4, "image/jpeg;base64")
  ]
  id = models.AutoField(primary_key=True)
  post = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE)
  author = models.ForeignKey(Author, blank=False, null=False, on_delete=models.CASCADE)
  content_type = models.IntegerField(choices=CONTENT_TYPE, blank=False, null=False)
  content = models.TextField(blank=False, null=False)
  published_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)