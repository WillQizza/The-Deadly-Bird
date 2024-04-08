from django.conf import settings
from rest_framework import serializers
from blue.models import Subscription
from posts.models import Post, Comment
from likes.models import Like
from following.models import Following, FollowingRequest
from .models import Author, InboxMessage
from nodes.models import Node
from deadlybird.util import resolve_remote_route, remove_trailing_slash
from urllib.parse import urljoin

class AuthorSerializer(serializers.ModelSerializer):
  """
  Serialize a author.
  """
  type = serializers.CharField(read_only=True, default='author')
  displayName = serializers.CharField(source='display_name')
  profileImage = serializers.SerializerMethodField()
  url = serializers.CharField(source='profile_url')
  posts = serializers.SerializerMethodField()
  followers = serializers.SerializerMethodField()
  following = serializers.SerializerMethodField()
  email = serializers.SerializerMethodField()
  subscribed = serializers.SerializerMethodField()

  def get_posts(self, obj: Author) -> int:
    return Post.objects.filter(author=obj).count()
  
  def get_followers(self, obj: Author) -> int:
    return Following.objects.filter(target_author=obj).count()

  def get_following(self, obj: Author) -> int:
    return Following.objects.filter(author=obj).count()
  
  def get_email(self, obj: Author) -> str|None:
    if "id" in self.context and obj.id == self.context["id"]:
      # Only return the user's email if they are the one requesting it
      return obj.user.email
    return None
  
  def get_profileImage(self, obj: Author) -> str:
    if (obj.profile_picture is not None) and len(obj.profile_picture) > 0:
      # Return saved avatar
      return obj.profile_picture
    else:
      # Return default avatar
      return urljoin(settings.SITE_HOST_URL, "/static/default-avatar.png")
    
  def get_subscribed(self, obj: Author) -> bool:
    try:
      Subscription.objects.get(author=obj)
      return True
    except Subscription.DoesNotExist:
      return False
    
  def to_internal_value(self, data):
    internal_data = super().to_internal_value(data)
    internal_data["id"] = remove_trailing_slash(internal_data["id"]).split("/")[:-1]
    if "github" in internal_data and internal_data["github"] is not None and internal_data["github"].startswith("https://github.com/"):
      internal_data["github"] = internal_data["github"][len("https://github.com/"):]
    internal_data["host"] = remove_trailing_slash(internal_data["host"]) + "/"
    return internal_data
  
  def to_representation(self, instance):
    data = super().to_representation(instance)
    data["id"] = resolve_remote_route(data["host"], "author", kwargs={ "author_id": data["id"] }, force_no_slash=True)
    if "github" in data and data["github"] is not None:
      data["github"] = f"https://github.com/{data['github']}"
    data["host"] = remove_trailing_slash(data["host"]) + "/"
    return data

  class Meta:
    model = Author
    fields = ['type', 'id', 'url', 'host', 'email', 'subscribed', 'bio', 'displayName', 'github', 'profileImage', 'posts', 'followers', 'following']

class InboxMessageSerializer(serializers.Serializer):
  """
  Serialize a inbox message.
  Items field is a list of heterogenous serialized objects.
  """

  def to_representation(self, instance):
    if instance.content_type == InboxMessage.ContentType.POST:
      from posts.serializers import PostSerializer
      post = Post.objects.get(id=instance.content_id)
      serializer = PostSerializer(instance=post)
      return serializer.data
    elif instance.content_type == InboxMessage.ContentType.FOLLOW:
      from following.serializers import FollowRequestSerializer
      request = FollowingRequest.objects.get(id=instance.content_id)
      serializer = FollowRequestSerializer(instance=request)
      return serializer.data
    elif instance.content_type == InboxMessage.ContentType.LIKE:
      from likes.serializers import LikeSerializer
      like = Like.objects.get(id=instance.content_id)
      serializer = LikeSerializer(instance=like)
      return serializer.data
    elif instance.content_type == InboxMessage.ContentType.COMMENT:
      from posts.serializers import CommentSerializer
      comment = Comment.objects.get(id=instance.content_id)
      serializer = CommentSerializer(instance=comment)
      return serializer.data

    return super().to_representation(instance)
  
class InboxAuthorSerializer(serializers.Serializer):
  """
  Validates a payload is a inbox author payload without the
  unique constraints of the models getting in the way
  """
  type = serializers.CharField(read_only=True, default="author")
  id = serializers.SerializerMethodField()
  github = serializers.CharField(required=False, allow_null=True, allow_blank=True)
  host = serializers.URLField()
  displayName = serializers.CharField(source="display_name")
  url = serializers.URLField(source="profile_url")
  profileImage = serializers.SerializerMethodField()

  def get_id(self, obj) -> str:
    if isinstance(obj, Author):
      return resolve_remote_route(obj.host, "author", kwargs={ "author_id": obj.id }, force_no_slash=True)
    else:
      return resolve_remote_route(obj["host"], "author", kwargs={ "author_id": obj["id"] }, force_no_slash=True)
    
  def get_profileImage(self, obj) -> str:
    if isinstance(obj, Author):
      profile_picture = obj.profile_picture
    elif "profile_picture" in obj:
      profile_picture = obj["profile_picture"]    

    if profile_picture is not None and len(profile_picture) > 0:
      return profile_picture
    else:
      # Return default avatar
      return settings.SITE_HOST_URL + "static/default-avatar.png"
    
  def to_representation(self, instance):
    data = super().to_representation(instance)
    data["host"] = remove_trailing_slash(data["host"]) + "/"
    return data

  def to_internal_value(self, data):
    return_data = super().to_internal_value(data)
    return_data["profile_picture"] = data["profileImage"]
    return_data["host"] = remove_trailing_slash(return_data["host"]) + "/"

    if "github" in return_data and return_data["github"] is not None and return_data["github"].startswith("https://github.com/"):
      return_data["github"] = return_data["github"][len("https://github.com/"):]
    return_data["id"] = remove_trailing_slash(data["id"]).split("/")[-1]

    return return_data