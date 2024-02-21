from rest_framework import serializers
from posts.models import Post
from following.models import Following, FollowingRequest
from .models import Author, InboxMessage
from typing import List

class AuthorSerializer(serializers.ModelSerializer):
  type = serializers.ReadOnlyField(default='author')
  displayName = serializers.CharField(source='user.username')
  profileImage = serializers.CharField(source='profile_picture')
  url = serializers.CharField(source='profile_url')
  posts = serializers.SerializerMethodField()
  followers = serializers.SerializerMethodField()
  following = serializers.SerializerMethodField()
  email = serializers.SerializerMethodField()

  def get_posts(self, obj: Author):
    return Post.objects.filter(author=obj).count()
  
  def get_followers(self, obj: Author):
    return Following.objects.filter(target_author=obj).count()

  def get_following(self, obj: Author):
    return Following.objects.filter(author=obj).count()
  
  def get_email(self, obj: Author):
    if "id" in self.context and obj.id == self.context["id"]:
      # Only return the user's email if they are the one requesting it
      return obj.user.email
    return None

  class Meta:
    model = Author
    fields = ['type', 'id', 'url', 'host', 'email', 'bio', 'displayName', 'github', 'profileImage', 'posts', 'followers', 'following']

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
      # TODO: implement like 
      pass
    elif instance.content_type == InboxMessage.ContentType.COMMENT:
      pass

    return super().to_representation(instance)