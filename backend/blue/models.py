from django.db import models
from deadlybird.util import generate_next_id
from identity.models import Author

# Create your models here.
class PaymentSession(models.Model):
  id = models.CharField(primary_key=True, max_length=255)
  author = models.ForeignKey(Author, blank=False, null=False, on_delete=models.CASCADE)

class Subscription(models.Model):
  class Type(models.TextChoices):
    MONTHLY = "monthly"
    ANNUAL = "annual"
  id = models.CharField(primary_key=True, max_length=255, default=generate_next_id)
  author = models.ForeignKey(Author, blank=False, null=False, on_delete=models.CASCADE)
  type = models.CharField(choices=Type.choices, max_length=7, blank=False, null=False)

class Ad(models.Model):
  class ContentType(models.TextChoices):
    MARKDOWN = "text/markdown"
    PLAIN = "text/plain"
    APPLICATION_BASE64 = "application/base64"
    PNG_BASE64 = "image/png;base64"
    JPEG_BASE64 = "image/jpeg;base64"

  id = models.CharField(primary_key=True, max_length=255, default=generate_next_id)
  company = models.CharField(max_length=255, blank=False, null=False)
  title = models.CharField(max_length=255, blank=False, null=False)
  description = models.CharField(max_length=255, blank=False, null=False)
  content_type = models.CharField(choices=ContentType.choices, max_length=30, blank=False, null=False)
  content = models.TextField(blank=False, null=False)