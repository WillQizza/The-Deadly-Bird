from django.db import models
from identity.models import Author
from posts.models import Post
from deadlybird.util import generate_next_id

# Create your models here.
class Like(models.Model):
  id = models.CharField(primary_key=True, max_length=10, default=generate_next_id)
  post = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE)
  author = models.ForeignKey(Author, blank=False, null=False, on_delete=models.CASCADE)