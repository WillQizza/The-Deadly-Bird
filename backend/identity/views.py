from django.contrib.auth.models import User
from django.http import HttpRequest
from django.conf import settings
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Author, InboxMessage
from deadlybird.util import generate_next_id, generate_full_api_url
from deadlybird.pagination import Pagination, generate_pagination_schema, generate_pagination_query_schema
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from .util import validate_login_session
from .pagination import InboxPagination, generate_inbox_pagination_query_schema, generate_inbox_pagination_schema
from .serializers import AuthorSerializer, InboxMessageSerializer

@extend_schema(
    responses=generate_pagination_schema("authors", AuthorSerializer(many=True)),
    parameters=generate_pagination_query_schema()
)
@api_view(["GET"])
def authors(request: HttpRequest):
  """
  Retrieve list of authors
  """
  authors = Author.objects.all().order_by("id")

  paginator = Pagination("authors")
  page = paginator.paginate_queryset(authors, request)

  our_user_id = request.session["id"] if (request.session.has_key("id")) else None
  serializer = AuthorSerializer(page, many=True, context={ "id": our_user_id })
  return paginator.get_paginated_response(serializer.data)

AuthorsFailResponseSerializer = inline_serializer("AuthorsFailResponse", fields={
  "message": serializers.CharField()
})
@extend_schema(
    methods=["GET", "PUT"],
    responses={
      200: AuthorSerializer(),
      404: AuthorsFailResponseSerializer,
      403: AuthorsFailResponseSerializer
    },
    parameters=[
      OpenApiParameter(name="author_id", location=OpenApiParameter.PATH, description="The author id to interact with")
    ]
)
@extend_schema(
  methods=["PUT"],
  request=inline_serializer("AuthorEditPayload", fields={
    "displayName": serializers.CharField(required=False),
    "password": serializers.CharField(required=False),
    "email": serializers.EmailField(required=False),
    "github": serializers.CharField(required=False),
    "profileImage": serializers.CharField(required=False),
    "bio": serializers.CharField(required=False)
  })
)
@api_view(["GET", "PUT"])
def author(request: HttpRequest, author_id: str):
  """
  Retrieve or edit a single author
  """
  if request.method == "GET":
    # Get profile
    try:
      author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
      return Response({
        "message": "No author found"
      }, status=404)

    our_user_id = request.session["id"] if (request.session.has_key("id")) else None
    serializer = AuthorSerializer(author, context={ "id": our_user_id })
    return Response(serializer.data)
  else:
    # Ensure that we are logged in while attempting to edit a user
    logged_in, response = validate_login_session(request)
    if not logged_in:
      return response

    try:
      author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
      return Response({
        "message": "No author found"
      }, status=404)
    
    if author.id != request.session["id"]:
      return Response({
        "message": "Cannot modify a different author"
      }, status=403)
    
    if "displayName" in request.POST:
      new_display_name = request.POST["displayName"]
      author.display_name = new_display_name
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
    if "bio" in request.POST:
      bio = request.POST["bio"]
      author.bio = bio

    author.user.save()
    author.save()

    response_serializer = AuthorSerializer(author)
    return Response(response_serializer.data)

@extend_schema(
    request=inline_serializer("LoginRequest", fields={
      "username": serializers.CharField(),
      "password": serializers.CharField()
    }),
    responses={
      400: inline_serializer("LoginFailure", fields={
        "authenticated": serializers.BooleanField(),
        "message": serializers.CharField()
      }),
      401: inline_serializer("LoginFailure", fields={
        "authenticated": serializers.BooleanField(),
        "message": serializers.CharField()
      }),
      200: inline_serializer("LoginSuccess", fields={
        "authenticated": serializers.BooleanField(),
        "id": serializers.CharField()
      })
    }
)
@api_view(["POST"])
def login(request: HttpRequest):
  if (not "username" in request.POST):
    return Response({
      "authenticated": False, 
      "message": "Username is required."
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

@extend_schema(
    request=inline_serializer("RegistrationDetails", fields={
      "username": serializers.CharField(),
      "password": serializers.CharField(),
      "email": serializers.CharField()
    }),
    responses={
      201: inline_serializer("RegistrationResponse", fields={
        "error": serializers.BooleanField(default=False),
        "message": serializers.CharField()
      }),
      400: inline_serializer("RegistrationError", fields={
        "error": serializers.BooleanField(),
        "message": serializers.CharField()
      }),
      409: inline_serializer("RegistrationError", fields={
        "error": serializers.BooleanField(),
        "message": serializers.CharField()
      })
    }
)
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
    display_name=created_user.username,
    host=settings.SITE_HOST_URL,
    profile_url=generate_full_api_url(view="author", kwargs={ "author_id": id })
  )
    
  # Send success
  return Response({
    "error": False,
    "message": "Success!"
  }, status=201)


@extend_schema(
  methods=["GET"],
  responses=generate_inbox_pagination_schema(),
  parameters=[
    OpenApiParameter(name="author_id", location=OpenApiParameter.PATH, description="The author id of the inbox to interact with"),
    *generate_inbox_pagination_query_schema()
  ]
)
@extend_schema(
  methods=["POST"],
  parameters=[
    OpenApiParameter(name="author_id", location=OpenApiParameter.PATH, description="The author id of the inbox to interact with")
  ] # TODO: Proper docs for inbox POST
)
@extend_schema(
  methods=["DELETE"],
  parameters=[
    OpenApiParameter(name="author_id", location=OpenApiParameter.PATH, description="The author id of the inbox to interact with")
  ],
  responses={
    204: inline_serializer("InboxDeleteSuccessResponse", fields={
            "error": serializers.BooleanField(default=False),
            "message": serializers.CharField()
          }),
    404: inline_serializer("InboxDeleteFailureResponse", fields={
            "error": serializers.BooleanField(),
            "message": serializers.CharField()
          })
  }
)
@api_view(["GET", "POST", "DELETE"])
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
    try:
      InboxMessage.objects.filter(author=author_id).delete()
      return Response({"error": False, "message": "inbox deleted"}, status=204)
    except:
      return Response({"error": True, "message": "unable to delete inbox"}, status=404)
