from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import serializers
from drf_spectacular.utils import inline_serializer, OpenApiParameter

class Pagination(PageNumberPagination):
    page_size = 10                  # default page size
    page_size_query_param = 'size'  # allow client to override the page size using this query parameter
    max_page_size = 100             # maximum limit of the page size

    def __init__(self, type) -> None:
        super().__init__()
        self.items_type = type


    def get_paginated_response(self, data):
        return Response({
            "type": self.items_type,
            "next": self.get_next_link(),
            "prev": self.get_previous_link(),
            "items": data
        })

def generate_pagination_schema(paginator_name: str, serializer: serializers.Serializer):
    return inline_serializer(
        name=f"Pagination_{paginator_name}",
        fields={
            "type": serializers.CharField(read_only=True, default=paginator_name),
            "next": serializers.CharField(allow_blank=True),
            "prev": serializers.CharField(allow_blank=True),
            "items": serializer
        }
    )

def generate_pagination_query_schema():
    return [
        OpenApiParameter(name="page", description="The page to retrieve items from", type=int, required=False, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="count", description="The amount of items to show per page", type=int, required=False, location=OpenApiParameter.QUERY)
    ]