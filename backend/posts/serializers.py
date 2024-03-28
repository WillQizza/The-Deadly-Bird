from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from identity.serializers import AuthorSerializer
from deadlybird.util import generate_full_api_url, remove_trailing_slash, resolve_remote_route
from .models import Post, Comment
from identity.serializers import InboxAuthorSerializer
from .pagination import generate_comments_pagination_schema


class CommentSerializer(serializers.ModelSerializer):
  type = serializers.CharField(read_only=True, default="comment")
  author = AuthorSerializer()
  comment = serializers.CharField(source="content")
  contentType = serializers.CharField(source="content_type")
  published = serializers.DateTimeField(source="published_date")

  class Meta:
    model = Comment
    fields = ["type", "id", "author", "comment", "contentType", "published"]

  def to_internal_value(self, data):
    internal_data = super().to_internal_value(data)
    internal_data["id"] = remove_trailing_slash(internal_data["id"]).split("/")[:-1]
    return internal_data
  
  def to_representation(self, instance):
    post_author_id = instance.post.author.id
    post_id = instance.post.id
    data = super().to_representation(instance)
    data["id"] = f'{generate_full_api_url("comments", kwargs={ "author_id": post_author_id, "post_id": post_id }, force_no_slash=True)}/{data["id"]}'
    return data

class PostSerializer(serializers.ModelSerializer):
  type = serializers.CharField(read_only=True, default="post")
  contentType = serializers.CharField(source="content_type")
  author = AuthorSerializer()
  originAuthor = AuthorSerializer(source="origin_author")
  originId = serializers.SerializerMethodField()
  count = serializers.SerializerMethodField()
  comments = serializers.SerializerMethodField()
  commentsSrc = serializers.SerializerMethodField()
  published = serializers.DateTimeField(source="published_date")

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
  
  def to_internal_value(self, data):
    internal_data = super().to_internal_value(data)
    internal_data["id"] = remove_trailing_slash(internal_data["id"]).split("/")[-1]
    internal_data["source"] = remove_trailing_slash(internal_data["source"])
    internal_data["origin"] = remove_trailing_slash(internal_data["origin"])
    return internal_data
  
  def to_representation(self, instance: Post):
    author_id = instance.author.id
    data = super().to_representation(instance)
    if instance.origin_post is not None:
      data["id"] = resolve_remote_route(instance.author.host, "post", kwargs={ "author_id": instance.origin_post.author.id, "post_id": instance.origin_post.id }, force_no_slash=True)
    else:
      data["id"] = generate_full_api_url("post", kwargs={ "author_id": author_id, "post_id": data["id"] }, force_no_slash=True)
    return data

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

  def to_internal_value(self, data):
    internal_data = super().to_internal_value(data)
    internal_data["id"] = internal_data["id"].split("/")[-1]
    internal_data["origin"] = remove_trailing_slash(internal_data["origin"])
    internal_data["source"] = remove_trailing_slash(internal_data["source"])
    return internal_data

class InboxCommentSerializer(serializers.Serializer):
  """
  Validate a payload is a inbox comment payload with the
  unique constraints of the models getting in the way.
  """
  type = serializers.CharField(read_only=True, default="comment")
  id = serializers.CharField()
  author = InboxAuthorSerializer()
  comment = serializers.CharField(source="content")
  contentType = serializers.CharField(source="content_type")
  published = serializers.DateTimeField(source="published_date")

  def to_internal_value(self, data):
    internal_data = super().to_internal_value(data)
    internal_data["id"] = remove_trailing_slash(internal_data["id"])
    return internal_data