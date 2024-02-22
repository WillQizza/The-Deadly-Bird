from django.db import models
from identity.models import Author
from deadlybird.util import generate_next_id

# Create your models here.
class Following(models.Model):
  id = models.CharField(primary_key=True, max_length=10, default=generate_next_id)
  target_author = models.ForeignKey(Author, 
                                    blank=False, 
                                    null=False, 
                                    on_delete=models.CASCADE, 
                                    related_name="following_to")
  author = models.ForeignKey(Author, 
                             blank=False, 
                             null=False, 
                             on_delete=models.CASCADE, 
                             related_name="following_from")

class FollowingRequest(models.Model):
  id = models.CharField(primary_key=True, max_length=10, default=generate_next_id)
  target_author = models.ForeignKey(Author, 
                                    blank=False, 
                                    null=False, 
                                    on_delete=models.CASCADE, 
                                    related_name="request_to")
  author = models.ForeignKey(Author, 
                             blank=False, 
                             null=False, 
                             on_delete=models.CASCADE, 
                             related_name="request_from")

