from django.contrib import admin
from .models import PaymentSession, Subscription

# Register your models here.
admin.site.register(PaymentSession)
admin.site.register(Subscription)