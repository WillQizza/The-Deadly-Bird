from django.contrib import admin
from .models import PaymentSession, Subscription, Ad

# Register your models here.
admin.site.register(PaymentSession)
admin.site.register(Subscription)
admin.site.register(Ad)