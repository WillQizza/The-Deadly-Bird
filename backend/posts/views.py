from django.http import HttpRequest
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import PostSerializer
from .models import Post

@api_view(["GET", "POST"])
def posts(request: HttpRequest, author_id: int):
  if request.method == 'GET':
    # Retrieve author posts
    # Special case where they request 0 (or less) as the size for some reason
    try:
      if "size" in request.GET and int(request.GET["size"]) <= 0:
        return Response([])
    except ValueError:
      return Response([])

    # Init paginator
    paginator = PageNumberPagination()
    paginator.page_size_query_param = "size"

    # TODO: When authentication is implemented, update this to include other visibilities if user can see
    # Retrieve and serialize posts that should be shown
    posts = Post.objects.all() \
              .filter(author=author_id, visibility=Post.Visibility.PUBLIC) \
              .order_by("-published_date")
    posts_on_page = paginator.paginate_queryset(posts, request)
    serialized_posts = PostSerializer(posts_on_page, many=True)

    # Output to user
    return Response(serialized_posts.data)
  else:
    # TODO: Create new post route
    pass