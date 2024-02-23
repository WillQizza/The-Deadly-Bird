from rest_framework import serializers
from identity.models import Author
from identity.serializers import AuthorSerializer

class LikeSerializer(serializers.Serializer):
    """
    Serialize a single Like object. 
    """
    type = serializers.CharField(default="Like", read_only=True)
    context = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    object = serializers.SerializerMethodField()

    def get_context(self, obj):
        # TODO: figure out what context field is
        return "Context"

    def get_author(self, obj):
        author = AuthorSerializer(obj.send_author)
        return author.data

    def get_summary(self, obj):
        return f"{obj.send_author.user} Likes your post"

    def get_object(self, obj):
        author: Author = obj.send_author
        return f"{author.host}/authors/{author.id}/posts/{obj.id}" 
    
    class Meta:
        fields = ['context', 'summary', 'type', 'author', 'object']