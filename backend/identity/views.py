from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Author, InboxMessage
from deadlybird.permissions import RemoteOrSessionAuthenticated, SessionAuthenticated, IsGetRequest, IsPutRequest, IsPostRequest, IsDeleteRequest
from deadlybird.serializers import GenericErrorSerializer, GenericSuccessSerializer
from deadlybird.util import generate_next_id, generate_full_api_url
from deadlybird.pagination import Pagination, generate_pagination_schema, generate_pagination_query_schema
from deadlybird.settings import SITE_HOST_URL
from likes.serializers import APIDocsLikeSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from .pagination import InboxPagination, generate_inbox_pagination_query_schema, generate_inbox_pagination_schema
from .serializers import AuthorSerializer, InboxMessageSerializer 
from identity.util import get_this_host_url

@extend_schema(
    operation_id="api_authors_retrieve_all",
    responses=generate_pagination_schema("authors", AuthorSerializer(many=True)),
    parameters=generate_pagination_query_schema()
)
@api_view(["GET"])
@permission_classes([RemoteOrSessionAuthenticated])
def authors(request: HttpRequest):
  """
  Retrieve list of authors
  """
 
  # Get author queryset ordered by their id
  authors = Author.objects.all().order_by("id")

  # Get query parameter filter if exists
  include_host_filter = request.query_params.get('include_host', None)
  exclude_host_filter = request.query_params.get('exclude_host', None)
  if include_host_filter:
    # authors = authors.filter(host=include_host_filter)
    authors = authors.filter(host__icontains=include_host_filter)
  elif exclude_host_filter:
    authors = authors.exclude(host__icontains=exclude_host_filter)

  if hasattr(request, "is_node_authenticated") and request.is_node_authenticated:
    authors = authors.filter(host=SITE_HOST_URL)

  # Paginate the queryset
  paginator = Pagination("authors")
  page = paginator.paginate_queryset(authors, request)

  # LOGGING
  print("get authors: ", include_host_filter, exclude_host_filter)

  # Return serialized result
  our_user_id = request.session["id"] if (request.session.has_key("id")) else None
  serializer = AuthorSerializer(page, many=True, context={ "id": our_user_id })
  return paginator.get_paginated_response(serializer.data)

@extend_schema(
    methods=["GET", "PUT"],
    responses={
      200: AuthorSerializer(),
      401: GenericErrorSerializer,
      404: GenericErrorSerializer,
      403: GenericErrorSerializer
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
@permission_classes([ (IsGetRequest & RemoteOrSessionAuthenticated) | (IsPutRequest & SessionAuthenticated) ])
def author(request: HttpRequest, author_id: str):
  """
  Retrieve or edit a single author
  """
  if request.method == "GET":
    # Try to get profile from author id
    try:
      author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
      return Response({
        "error": True,
        "message": "No author found"
      }, status=404)

    # Return serialized profile
    our_user_id = request.session["id"] if (request.session.has_key("id")) else None
    serializer = AuthorSerializer(author, context={ "id": our_user_id })
    return Response(serializer.data)
  else: 
    # Retrieve author to edit
    try:
      author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
      return Response({
        "error": True,
        "message": "No author found"
      }, status=404)
    
    if author.id != request.session["id"]:
      return Response({
        "error": True,
        "message": "Cannot modify a different author"
      }, status=403)

    # Store error message if any properties do not match property limits
    error = None
    
    # Update display name
    if "displayName" in request.POST:
      new_display_name = request.POST["displayName"]
      if (0 < len(new_display_name) < 255):
        author.display_name = new_display_name
      else:
        error = "Invalid display name length"

    # Update password
    if "password" in request.POST:
      password = request.POST["password"]
      author.user.set_password(password)

    # Update email
    if "email" in request.POST:
      email = request.POST["email"]
      if (0 < len(email) < 254):
        author.user.email = email
      else:
        error = "Invalid email length"

    # Update github
    if "github" in request.POST:
      github = request.POST["github"]
      if (len(github) < 254):
        author.github = github
      else:
        error = "Invalid github length"

    # Update profile image
    if "profileImage" in request.POST:
      profile_picture = request.POST["profileImage"]
      if (0 < len(profile_picture) < 255):
        author.profile_picture = profile_picture
      else:
        error = "Invalid profile picture length"

    # Update bio
    if "bio" in request.POST:
      bio = request.POST["bio"]
      if (0 <= len(bio) < 255):
        author.bio = bio
      else:
        error = "Invalid bio length"

    # Return error if exists
    if (error is not None):
      return Response({
        "error": True,
        "message": error
      }, status=400)

    # Save updates
    author.user.save()
    author.save()

    response_serializer = AuthorSerializer(author)
    return Response(response_serializer.data)

LoginFailureSerializer = inline_serializer("LoginFailure", fields={
  "authenticated": serializers.BooleanField(),
  "message": serializers.CharField()
})
@extend_schema(
    request=inline_serializer("LoginRequest", fields={
      "username": serializers.CharField(),
      "password": serializers.CharField()
    }),
    responses={
      400: LoginFailureSerializer,
      401: LoginFailureSerializer,
      200: inline_serializer("LoginSuccess", fields={
        "authenticated": serializers.BooleanField(),
        "id": serializers.CharField()
      })
    }
)
@api_view(["POST"])
def login(request: HttpRequest):
  # Check for required credentials
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
  
  # Get credentials
  username = request.POST["username"]
  password = request.POST["password"]
  
  # Find user
  try:
    user = User.objects.get(username__iexact=username)
  except User.DoesNotExist:
    return Response({
      "authenticated": False,
      "message": "Invalid username or password. Please try again."
    }, status=401)

  # Check password
  password_matches = user.check_password(password)
  if not password_matches:
    return Response({
      "authenticated": False,
      "message": "Invalid username or password. Please try again."
    }, status=401)
  
  # Check if activated
  if not user.is_active:
    return Response({
      "authenticated": False,
      "message": "Account not activated. Contact admin to activate."
    }, status=403)

  # Start session
  author = Author.objects.get(user=user)
  request.session["id"] = author.id

  return Response({
    "authenticated": True,
    "id": request.session["id"]
  })

@api_view(["POST"])
def logout(request: HttpRequest):
  request.session.flush()
  return Response({
    "success": True
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
      400: GenericErrorSerializer,
      409: GenericErrorSerializer
    }
)
@api_view(["POST"])
def register(request: HttpRequest):
  # Check for required credentials
  if (not "username" in request.POST) or (not "password" in request.POST) or (not "email" in request.POST):
    return Response({
      "error": True,
      "message": "No credentials provided"
    }, status=400)
  
  # Get credentials
  username = request.POST["username"]
  password = request.POST["password"]
  email = request.POST["email"]

  # Check credential lengths
  if not (0 < len(request.POST["username"]) < 150) \
    or not (0 < len(request.POST["email"]) < 254):
    return Response({
      "error": True,
      "message": "Invalid credential length"
    }, status=400)

  # Check if an user already exists with that username
  try:
    User.objects.get(username__iexact=username)
    return Response({
      "error": True,
      "message": "Account already exists"
    }, status=409)
  except User.DoesNotExist:
    pass
  # Check if an user already exists with that email
  try:
    User.objects.get(email__iexact=email)
    return Response({
      "error": True,
      "message": "Account already exists"
    }, status=409)
  except:
    pass
  
  # Create user object (default inactive)
  created_user = User.objects.create_user(username=username, email=email, password=password)
  created_user.is_active = False
  created_user.save()

  # Create author object from user object
  id = generate_next_id()
  Author.objects.create(
    id=id,
    user=created_user,
    display_name=created_user.username,
    host=get_this_host_url(),
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
  ],
  request=APIDocsLikeSerializer,  # Example used in the docs for specs
  responses={
    400: GenericErrorSerializer,
    201: GenericSuccessSerializer
  }
)
@extend_schema(
  methods=["DELETE"],
  parameters=[
    OpenApiParameter(name="author_id", location=OpenApiParameter.PATH, description="The author id of the inbox to interact with")
  ],
  responses={
    204: GenericSuccessSerializer,
    404: GenericErrorSerializer,
    409: GenericErrorSerializer
  }
)
@api_view(["GET", "POST", "DELETE"])
@permission_classes([ (IsGetRequest & SessionAuthenticated) | (IsPostRequest & RemoteOrSessionAuthenticated) | (IsDeleteRequest & SessionAuthenticated) ])
def inbox(request: HttpRequest, author_id: str):
  """
  URL: ://service/authors/{AUTHOR_ID}/inbox
  GET [local]: if authenticated get a paginated list of posts sent to AUTHOR_ID
  POST [local, remote]: send a post to the author
  DELETE [local]: clear the inbox
  """
  if request.method == "POST":
    # Check request data
    content_type = request.data.get("type")
    print("INBOX REQUEST RECEIVED WITH TYPE " + content_type)
    print(request.data)

    if content_type == None:
      return Response({
        "error": True,
        "message": "Missing necessary request body parameters"
      }, status=400)
    
    if content_type == "Like":
      # Ensure like data is valid data
      from .inbox import handle_like_inbox
      return handle_like_inbox(request)
    elif content_type == "post":
      from .inbox import handle_post_inbox
      return handle_post_inbox(request, target_author_id=author_id)

    elif content_type == "Follow": 
      from .inbox import handle_follow_inbox
      return handle_follow_inbox(request)

    elif content_type == "Unfollow":
      from .inbox import handle_unfollow_inbox
      return handle_unfollow_inbox(request)

    elif content_type == "FollowResponse":
      from .inbox import handle_follow_response_inbox
      return handle_follow_response_inbox(request)

    elif content_type == "comment":
      from .inbox import handle_comment_inbox
      return handle_comment_inbox(request)
    
    else:
      return Response({ "error": True, "message": "Unknown inbox type" }, status=400)
  
  if request.method == "GET":
    # Return the list of inbox messages for the author   
    inbox_messages = InboxMessage.objects.filter(author=author_id).order_by("id")
    paginator = InboxPagination(author_id=author_id)
    page = paginator.paginate_queryset(inbox_messages, request)
    serializer = InboxMessageSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)
  
  if request.method == "DELETE":
    # Delete inbox messages of the author
    try:
      InboxMessage.objects.filter(author=author_id).delete()
      return Response({"error": False, "message": "inbox deleted"}, status=204)
    except:
      return Response({"error": True, "message": "unable to delete inbox"}, status=404)
