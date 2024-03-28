from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Following, FollowingRequest
from identity.models import Author
from identity.serializers import AuthorSerializer

class FollowingSerializer(serializers.Serializer):
    type = serializers.CharField(default="followers", read_only=True)
    items = serializers.SerializerMethodField()

    @extend_schema_field(field=AuthorSerializer(many=True))
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
    type = serializers.CharField(default="Follow", read_only=True)
    summary = serializers.SerializerMethodField()
    object = AuthorSerializer(source="target_author")
    actor = AuthorSerializer(source="author")

    def get_summary(self, obj):
        return f"{obj.author.display_name} wants to follow {obj.target_author.display_name}"
    
    class Meta:
        fields = ['type', 'summary', 'object', 'actor']