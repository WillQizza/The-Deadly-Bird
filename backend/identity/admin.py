from django.contrib import admin
from .models import Author, InboxMessage

# Register your models here.
admin.site.register(Author)
admin.site.register(InboxMessage)