from rest_framework import serializers
from deadlybird.util import generate_full_api_url, get_host_with_slash
from deadlybird.settings import SITE_HOST_URL
from identity.serializers import AuthorSerializer
from identity.models import Author
from drf_spectacular.utils import inline_serializer
from .models import Like
from posts.models import Post, Comment

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
        if obj.content_type == Like.ContentType.POST:
            return f"{obj.send_author.display_name} likes your post"
        else:
            return f"{obj.send_author.display_name} likes your comment"

    def get_object(self, obj: Like) -> str:
        if obj.content_type == Like.ContentType.POST:
            post = Post.objects.get(id=obj.content_id)
            return generate_full_api_url("post", kwargs={ "author_id": post.author.id, "post_id": post.id })
        else:
            comment = Comment.objects.get(id=obj.content_id)
            return f"{get_host_with_slash(SITE_HOST_URL)}api/authors/{comment.post.author.id}/posts/{comment.post.id}/comments/{comment.id}"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["@context"] = data.pop("context")
        return data
    
    class Meta:
        model = Like
        fields = ['context', 'summary', 'type', 'author', 'object']

APIDocsLikeSerializer = inline_serializer("APILike", fields={
    "type": serializers.CharField(default="Like", read_only=True),
    "@context":  serializers.CharField(),
    "summary":  serializers.CharField(),
    "author": AuthorSerializer(),
    "object": serializers.CharField()
})
APIDocsLikeManySerializer = inline_serializer("APILike", fields={
    "type": serializers.CharField(default="Like", read_only=True),
    "@context":  serializers.CharField(),
    "summary":  serializers.CharField(),
    "author": AuthorSerializer(),
    "object": serializers.CharField()
})