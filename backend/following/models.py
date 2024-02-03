from django.db import models
from identity.models import Author

# Create your models here.
class Following(models.Model):
  id = models.AutoField(primary_key=True)
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
  id = models.AutoField(primary_key=True)
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

