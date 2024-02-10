from rest_framework import serializers
from .models import Following, FollowingRequest
from identity.serializers import AuthorSerializer

class FollowingSerializer(serializers.Serializer):
    type = serializers.CharField(default="followers", read_only=True)
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