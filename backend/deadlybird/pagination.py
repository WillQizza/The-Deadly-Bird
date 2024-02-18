from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class Pagination(PageNumberPagination):
    page_size = 10                  # default page size
    page_size_query_param = 'size'  # allow client to override the page size using this query parameter
    max_page_size = 100             # maximum limit of the page size

    def __init__(self, type: str) -> None:
        super().__init__()
        self.items_type = type


    def get_paginated_response(self, data):
        return Response({
            "type": self.items_type,
            "next": self.get_next_link(),
            "prev": self.get_previous_link(),
            "items": data
        })