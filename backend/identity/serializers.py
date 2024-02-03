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