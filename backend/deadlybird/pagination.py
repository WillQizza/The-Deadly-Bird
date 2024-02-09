from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10                  # default page size
    page_size_query_param = 'size'  # allow client to override the page size using this query parameter
    max_page_size = 100             # maximum limit of the page size