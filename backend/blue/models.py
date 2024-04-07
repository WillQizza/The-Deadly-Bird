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