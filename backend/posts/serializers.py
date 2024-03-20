from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from identity.serializers import AuthorSerializer
from deadlybird.util import generate_full_api_url
from .models import Post, Comment
from identity.serializers import InboxAuthorSerializer
from .pagination import generate_comments_pagination_schema

class CommentSerializer(serializers.ModelSerializer):
  type = serializers.CharField(read_only=True, default="comment")
  author = serializers.SerializerMethodField()
  comment = serializers.CharField(source="content")
  contentType = serializers.CharField(source="content_type")
  published = serializers.DateTimeField(source="published_date")

  def get_author(self, object: Comment) -> AuthorSerializer: # This typing is purposely wrong so that the drf can serialize the docs correctly
    serializer = AuthorSerializer(object.author)
    return serializer.data

  class Meta:
    model = Comment
    fields = ["type", "id", "author", "comment", "contentType", "published"]

class PostSerializer(serializers.ModelSerializer):
  type = serializers.CharField(read_only=True, default="post")
  contentType = serializers.CharField(source="content_type")
  author = serializers.SerializerMethodField()
  originAuthor = serializers.SerializerMethodField()
  originId = serializers.SerializerMethodField()
  count = serializers.SerializerMethodField()
  comments = serializers.SerializerMethodField()
  commentsSrc = serializers.SerializerMethodField()
  published = serializers.DateTimeField(source="published_date")

  def get_author(self, object: Post) -> AuthorSerializer: # This typing is purposely wrong so that the drf can serialize the docs correctly
    return AuthorSerializer(object.author).data
  
  def get_originAuthor(self, object: Post) -> AuthorSerializer:
    if object.origin_author != None:
      return AuthorSerializer(object.origin_author).data
    return None
  
  def get_originId(self, object: Post) -> str:
    if object.origin_post != None:
      return object.origin_post.id
    return None
    
  def get_count(self, object: Post) -> int:
    return Comment.objects.filter(post=object).count()
  
  def get_comments(self, object: Post) -> str:
    return generate_full_api_url("comments", kwargs={ "author_id": object.author.id, "post_id": object.id })
  
  @extend_schema_field(field=generate_comments_pagination_schema())
  def get_commentsSrc(self, object: Post) -> None:
    return {
      'type': 'comments',
      'page': 1,
      'size': 5,
      'post': object.id,
      'id': object.id,
      'comments': CommentSerializer(Comment.objects.filter(post=object).order_by("-published_date")[:5], many=True).data
    }

  class Meta:
    model = Post
    fields = ['type', 'title', 'id', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'count', 'comments', 'commentsSrc', 'published', 'visibility', 'originAuthor', 'originId']

class InboxPostSerializer(serializers.Serializer):
  """
  Validates a payload is a inbox post payload without the
  unique constraints of the models getting in the way
  """
  type = serializers.CharField(read_only=True, default="post")
  id = serializers.CharField()
  title = serializers.CharField()
  description = serializers.CharField()
  source = serializers.URLField()
  origin = serializers.URLField()
  content = serializers.CharField()
  contentType = serializers.CharField(source="content_type")
  author = InboxAuthorSerializer()
  published = serializers.DateTimeField(source="published_date")
  visibility = serializers.ChoiceField(choices=Post.Visibility.values)