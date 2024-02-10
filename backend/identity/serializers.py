from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
  type = serializers.ReadOnlyField(default='author')
  displayName = serializers.CharField(source='user.username')
  profileImage = serializers.CharField(source='profile_picture')
  url = serializers.CharField(source='profile_url')

  class Meta:
    model = Author
    fields = ['type', 'id', 'url', 'host', 'displayName', 'github', 'profileImage']

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