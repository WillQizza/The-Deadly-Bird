from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post

@api_view(["GET", "POST"])
def posts(request: HttpRequest, author_id: int):
  if request.method == 'GET':
    # Retrieve author posts
    # TODO: Pagination support

    # TODO: Show ALL posts if authenticated
    posts = Post.objects.all().filter(author=author_id, visibility=Post.Visibility.PUBLIC)
    return Response(len(posts))
  else:
    # TODO: Create new post route
    pass