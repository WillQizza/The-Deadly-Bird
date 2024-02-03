from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Author
from .serializers import AuthorSerializer

# Create your views here.
@api_view(["GET", "POST"])
def author(request: HttpRequest, author_id: int):
  if request.method == "GET":
    # Get profile
    author = get_object_or_404(Author, id=author_id)

    serializer = AuthorSerializer(author)
    return Response(serializer.data)
  else:
    # Update profile
    pass