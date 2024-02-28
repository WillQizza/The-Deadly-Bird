from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from identity.serializers import AuthorSerializer
from typing import List
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
  type = serializers.CharField(read_only=True, default="post")
  contentType = serializers.CharField(source="content_type")
  author = serializers.SerializerMethodField()
  count = serializers.SerializerMethodField()
  comments = serializers.SerializerMethodField()
  commentsSrc = serializers.SerializerMethodField()
  published = serializers.DateTimeField(source="published_date")

  def get_author(self, object: Post) -> AuthorSerializer: # This typing is purposely wrong so that the drf can serialize the docs correctly
    return AuthorSerializer(object.author).data

  def get_count(self, object: Post) -> int:
    return Comment.objects.filter(post=object).count()
  
  def get_comments(self, object: Post) -> str:
    return None # TODO: (currently sets null)
    # TODO: URL to comments
  
  def get_commentsSrc(self, object: Post) -> None:
    return None # TODO: (currently sets null)
    # TODO: 5 comments sorted newest to oldest in the api spec format
    return {
      'type': 'comments',
      'page': 1,
      'size': 5,
      'post': '',  # TODO: URL to post?
      'id': '', # TODO: ??? Comments page id?...
      'comments': []  # TODO: Get and serialize comments
    }

  class Meta:
    model = Post
    fields = ['type', 'title', 'id', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'count', 'comments', 'commentsSrc', 'published', 'visibility']
