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

  def get_posts(self, obj: Author):
    return Post.objects.filter(author=obj).count()
  
  def get_followers(self, obj: Author):
    return Following.objects.filter(target_author=obj).count()

  def get_following(self, obj: Author):
    return Following.objects.filter(author=obj).count()

  class Meta:
    model = Author
    fields = ['type', 'id', 'url', 'host', 'displayName', 'github', 'profileImage', 'posts', 'followers', 'following']

class AuthorListSerializer(serializers.Serializer):
  """
  Serialize a list of authors into "type" and "items" fields for requirement
  """
  type = serializers.CharField(default="authors", read_only=True)
  items = serializers.SerializerMethodField()

  def get_items(self, obj):
    try:
      authors = [AuthorSerializer(author).data for author in obj]
      return authors
    except TypeError:
      author = AuthorSerializer(obj.author).data 
      return author

  class Meta:
      fields = ['type', 'items'] 

class InboxMessageListSerializer(serializers.Serializer):
  """
  Serialize a list of inbox mesasges.
  Items field is a list of heterogenous serialized objects.
  """
  type = serializers.CharField(default="inbox", read_only=True)
  author = serializers.CharField(read_only=True)
  items = serializers.SerializerMethodField()

  def get_items(self, inbox_messages: List[InboxMessage]):
    items = []
    for msg in inbox_messages:
      if msg.content_type == InboxMessage.ContentType.POST:
        from posts.serializers import PostSerializer
        post = Post.objects.get(id=msg.content_id)
        serializer = PostSerializer(instance=post)
        items.append(serializer.data)
      elif msg.content_type == InboxMessage.ContentType.FOLLOW:
        # TODO: this one is confusing since the follow object is not yet created.
        pass
      elif msg.content_type == InboxMessage.ContentType.LIKE:
        # TODO: implement like 
        pass
      elif msg.content_type == InboxMessage.ContentType.COMMENT:
        pass
    return items
  
  def to_representation(self, instance):
    ret = super().to_representation(instance)
    ret['author'] = self.context.get('author_id')
    return ret
  
  class Meta:
    fields = ['type', 'author', 'items']