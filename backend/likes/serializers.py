from rest_framework import serializers
from identity.serializers import AuthorSerializer
from drf_spectacular.utils import inline_serializer
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    """
    Serialize a single Like object. 
    """
    type = serializers.CharField(default="Like", read_only=True)
    context = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    author = AuthorSerializer(source="send_author")
    object = serializers.SerializerMethodField()

    def get_context(self, obj: Like) -> str:
        return "https://www.w3.org/ns/activitystreams"

    def get_summary(self, obj: Like) -> str:
        return f"{obj.send_author.user} Likes your post"

    def get_object(self, obj: Like) -> str:
        return obj.id
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["@context"] = data.pop("context")
        return data
    
    class Meta:
        model = Like
        fields = ['context', 'summary', 'type', 'author', 'object']

APIDocsLikeSerializer = inline_serializer("APILike", fields={
    "type": serializers.CharField(default="Like", read_only=True),
    "@context":  serializers.SerializerMethodField(),
    "summary":  serializers.SerializerMethodField(),
    "author": AuthorSerializer(),
    "object": serializers.CharField()
})
APIDocsLikeManySerializer = inline_serializer("APILike", fields={
    "type": serializers.CharField(default="Like", read_only=True),
    "@context":  serializers.SerializerMethodField(),
    "summary":  serializers.SerializerMethodField(),
    "author": AuthorSerializer(),
    "object": serializers.CharField()
})