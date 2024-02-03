from django.db import models

from identity.models import Author

# Create your models here.
class InboxMessage(models.Model):
  CONTENT_TYPE = [] # TODO: At some point this will need to be updated with things like (0, "like") (1, "post") and whatnot

  id = models.AutoField(primary_key=True)
  author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=False, null=False)
  content_id = models.IntegerField(blank=False, null=False)
  content_type = models.IntegerField(blank=False, null=False, choices=CONTENT_TYPE)