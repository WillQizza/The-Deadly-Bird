from django.contrib import admin
from .models import Following, FollowingRequest

# Register your models here.
admin.site.register(FollowingRequest)
admin.site.register(Following)