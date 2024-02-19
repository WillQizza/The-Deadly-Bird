from rest_framework import serializers
from .models import Following, FollowingRequest
from identity.models import Author
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

class FollowRequestSerializer(serializers.Serializer):
    """
    Serialize a single instance of a FollowRequest object. No support for
    many / paginated serialization for now.
    """
    type = serializers.CharField(default="follow_request", read_only=True)
    request_id = serializers.CharField(source="id")
    target_author = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    
    def get_target_author(self, obj):
        target_author = AuthorSerializer(obj.target_author)
        return target_author.data
    
    def get_author(self, obj):
        author = AuthorSerializer(obj.author)
        return author.data 
     
    class Meta:
        fields = ['type', 'id', 'author', 'target_author']