from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import serializers
from drf_spectacular.utils import inline_serializer, OpenApiParameter

class CommentsPagination(PageNumberPagination):
    page_size = 10                  # default page size
    page_size_query_param = 'size'  # allow client to override the page size using this query parameter
    max_page_size = 100             # maximum limit of the page size

    def get_paginated_response(self, data):
        return Response({
            "type": "comments",
            "post": "", # TODO: Replace with site host of post
            "id": "",   # TODO: Replace with site host of comments
            "next": self.get_next_link(),
            "prev": self.get_previous_link(),
            "comments": data,
            "page": 0,  # TODO: Replace with page
            "size": 0   # TODO: Replace with size
        })
    
def generate_comments_pagination_schema():
    from posts.serializers import CommentSerializer

    return inline_serializer(
        name=f"CommentPagination_Comments",
        fields={
            "type": serializers.CharField(read_only=True, default="comments"),
            "post": serializers.CharField(),
            "id": serializers.CharField(),
            "next": serializers.CharField(allow_blank=True),
            "prev": serializers.CharField(allow_blank=True),
            "comments": CommentSerializer(many=True),
            "page": serializers.IntegerField(),
            "size": serializers.IntegerField()
        }
    )

def generate_comments_pagination_query_schema():
    return [
        OpenApiParameter(name="page", description="The page to retrieve items from", type=int, required=False, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="count", description="The amount of items to show per page", type=int, required=False, location=OpenApiParameter.QUERY)
    ]