from rest_framework import serializers
from identity.models import Author
from identity.serializers import AuthorSerializer
from drf_spectacular.utils import inline_serializer

class LikeSerializer(serializers.Serializer):
    """
    Serialize a single Like object. 
    """
    type = serializers.CharField(default="Like", read_only=True)
    context = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    object = serializers.SerializerMethodField()

    def get_context(self, obj) -> str:
        return "https://www.w3.org/ns/activitystreams"

    def get_author(self, obj) -> AuthorSerializer: # This typing is purposely wrong so that the drf can serialize the docs correctly
        author = AuthorSerializer(obj.send_author)
        return author.data

    def get_summary(self, obj) -> str:
        return f"{obj.send_author.user} Likes your post"

    def get_object(self, obj) -> str:
        author: Author = obj.send_author
        return f"{author.host}/authors/{author.id}/posts/{obj.id}" # TODO: For part 2, check if this is meant to be author.host or SITE_HOST
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["@context"] = data.pop("context")
        return data
    
    class Meta:
        fields = ['@context', 'summary', 'type', 'author', 'object']

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