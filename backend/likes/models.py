from django.db import models
from identity.models import Author
from posts.models import Post

# Create your models here.
class Like(models.Model):
  id = models.AutoField(primary_key=True)
  post = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE)
  author = models.ForeignKey(Author, blank=False, null=False, on_delete=models.CASCADE)