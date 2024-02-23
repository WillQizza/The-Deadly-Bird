from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Author, InboxMessage
from .serializers import AuthorSerializer, InboxMessageSerializer
from deadlybird.util import generate_next_id, generate_full_api_url
from deadlybird.pagination import Pagination
from .pagination import InboxPagination

@api_view(["GET"])
def authors(request: HttpRequest):
  """
  get all authors view as to handle https://uofa-cmput404.github.io/general/project.html#authors
  """
  authors = Author.objects.all().order_by("id")

  paginator = Pagination("authors")
  page = paginator.paginate_queryset(authors, request)

  our_user_id = request.session["id"] if (request.session.has_key("id")) else None
  serializer = AuthorSerializer(page, many=True, context={ "id": our_user_id })
  return paginator.get_paginated_response(serializer.data)

@api_view(["GET", "PUT"])
def author(request: HttpRequest, author_id: str):
  if request.method == "GET":
    # Get profile
    author = get_object_or_404(Author, id=author_id)

    our_user_id = request.session["id"] if (request.session.has_key("id")) else None
    serializer = AuthorSerializer(author, context={ "id": our_user_id })
    return Response(serializer.data)
  else:
    author = Author.objects.get(id=request.session["id"])
    if ("displayName" in request.POST):
      new_username = request.POST["displayName"]
      author.user.username = new_username
    if "password" in request.POST:
      password = request.POST["password"]
      author.user.set_password(password)
    if "email" in request.POST:
      email = request.POST["email"]
      author.user.email = email
    if "github" in request.POST:
      github = request.POST["github"]
      author.github = github
    if "profileImage" in request.POST:
      profile_picture = request.POST["profileImage"]
      author.profile_picture = profile_picture

    author.user.save()
    author.save()

    return Response({
      "error": False,
      "message": "Success!"
    }, status=201)

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
  if (not "username" in request.POST) or (not "password" in request.POST) or (not "email" in request.POST):
    return Response({
      "error": True,
      "message": "No credentials provided"
    }, status=400)
  username = request.POST["username"]
  password = request.POST["password"]
  email = request.POST["email"]

  # Check if an user already exists with that username
  try:
    User.objects.get(username__iexact=username)
    return Response({
      "error": True,
      "message": "Account already exists"
    }, status=409)
  except User.DoesNotExist:
    pass
  try:
    User.objects.get(email__iexact=email)
    return Response({
      "error": True,
      "message": "Account already exists"
    }, status=409)
  except:
    pass
  
  # Create user object
  created_user = User.objects.create_user(username=username, email=email, password=password)

  # Create author object from user object
  id = generate_next_id()
  Author.objects.create(
    id=id,
    user=created_user,
    host=settings.SITE_HOST_URL,
    profile_url=generate_full_api_url(view="author", kwargs={ "author_id": id })
  )
    
  # Send success
  return Response({
    "error": False,
    "message": "Success!"
  }, status=201)


@api_view(["GET", "POST"])
def inbox(request: HttpRequest, author_id: str):
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
    paginator = InboxPagination(author_id=author_id)
    page = paginator.paginate_queryset(inbox_messages, request)
    serializer = InboxMessageSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)
  
  if request.method == "DELETE":
    #TODO: implement delete inbox (clear)
    pass