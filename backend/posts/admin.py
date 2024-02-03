from django.contrib import admin
from .models import Post, PostCategoryMeta, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(PostCategoryMeta)
admin.site.register(Comment)