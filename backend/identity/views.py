from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Author, InboxMessage
from .serializers import AuthorListSerializer, AuthorSerializer, InboxMessageListSerializer
from deadlybird.pagination import Pagination

@api_view(["GET"])
def authors(request):
  """
  get all authors view as to handle https://uofa-cmput404.github.io/general/project.html#authors
  """
  authors = Author.objects.all().order_by("id")

  paginator = Pagination()
  page = paginator.paginate_queryset(authors, request)
  
  if page is not None:
    serializer = AuthorListSerializer(page)
    return paginator.get_paginated_response(serializer.data)
 
  serializer = AuthorListSerializer(authors)
  return Response(serializer.data)  

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

@api_view(["POST"])
def login(request: HttpRequest):
  if (not "username" in request.POST):
    return Response({
      "authenticated": False, "message": "Username is required."
    }, status=400)
  if (not "password" in request.POST):
    return Response({
      "authenticated": False,
      "message": "Password is required."
    }, status=400)
  username = request.POST["username"]
  password = request.POST["password"]
  
  try:
    user = User.objects.get(username__iexact=username)
  except User.DoesNotExist:
    return Response({
      "authenticated": False,
      "message": "Invalid username or password. Please try again."
    }, status=401)

  password_matches = user.check_password(password)
  if not password_matches:
    return Response({
      "authenticated": False,
      "message": "Invalid username or password. Please try again."
    }, status=401)

  author = Author.objects.get(user=user)
  request.session["id"] = author.id

  return Response({
    "authenticated": True,
    "id": request.session["id"]
  })

@api_view(["POST"])
def register(request: HttpRequest):
  if (not "username" in request.POST) or (not "password" in request.POST):
    return Response({
      "error": True,
      "message": "No credentials provided"
    }, status=400)
  username = request.POST["username"]
  password = request.POST["password"]

  # Check if an user already exists with that username
  try:
    User.objects.get(username__iexact=username)
    return Response({
      "error": True,
      "message": "Account already exists"
    }, status=409)
  except User.DoesNotExist:
    pass
  
  # Create user object
  created_user = User.objects.create_user(username=username, password=password)

  # Create author object from user object
  Author.objects.create(
    user=created_user,
    host="http://localhost:8000",
    profile_url="http://localhost:8000"
  )
    
  # Send success
  return Response({
    "error": False,
    "message": "Success!"
  }, status=201)


@api_view(["GET", "POST"])
def inbox(request: HttpRequest, author_id: int):
  """
  URL: ://service/authors/{AUTHOR_ID}/inbox
  GET [local]: if authenticated get a paginated list of posts sent to AUTHOR_ID
  POST [local, remote]: send a post to the author
  DELETE [local]: clear the inbox
  """
  if request.method == "POST":
    # add a new inbox message item  
    content_type = request.data.get("content_type")
    content_id = request.data.get("content_id")

    if content_id == None or content_type == None:
      return Response({
        "error": True,
        "message": "Missing necessary request body parameters"
      }, status_code=400)

    try:
      InboxMessage.objects.create(
        author_id=author_id,
        content_id=content_id,
        content_type=content_type
      )
      return Response({
        "error": False,
        "message": "Created inbox message"
      }, status=201)
    except:
      return Response({
        "error": True,
        "message": "Failed to create inbox message"
      }, status=400)
  
  if request.method == "GET":
    # return the list of inbox messages for the author   
    inbox_messages = InboxMessage.objects.filter(author=author_id).order_by("id")
    paginator = Pagination()
    page = paginator.paginate_queryset(inbox_messages, request)
    serializer = InboxMessageListSerializer(instance=page, context={'author_id': author_id})

    return paginator.get_paginated_response(serializer.data)
  
  if request.method == "DELETE":
    #TODO: implement delete inbox (clear)
    pass