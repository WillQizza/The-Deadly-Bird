from rest_framework.permissions import BasePermission
from identity.models import Author

class SessionAuthenticated(BasePermission):
  """
  Handles permission requests in regards to a user needing to be logged in
  """
  
  def has_permission(self, request, view):
    if not "id" in request.session:
      return False
    
    try:
      Author.objects.get(id=request.session["id"])
    except Author.DoesNotExist:
      return False
    
    return True

class RemoteNodeAuthenticated(BasePermission):
  """
  Handles permission requests in regards to a user needing the correct credentials
  """

  def has_permission(self, request, view):
    return hasattr(request, "is_node_authenticated") and request.is_node_authenticated

class RemoteOrSessionAuthenticated(RemoteNodeAuthenticated):
  """
  Handles permission requests in regards to a user needing to be logged in
  or having the correct node credentials
  """

  def has_permission(self, request, view):
    session_authenticated = SessionAuthenticated().has_permission(request, view)
    return super().has_permission(request, view) or session_authenticated
  
class IsPostRequest(BasePermission):
  """
  Handles permission requests in regards to if a request is a POST request.
  """

  def has_permission(self, request, view):
    return request.method == "POST"

class IsGetRequest(BasePermission):
  """
  Handles permission requests in regards to if a request is a GET request.
  """

  def has_permission(self, request, view):
    return request.method == "GET"

class IsPutRequest(BasePermission):
  """
  Handles permission requests in regards to if a request is a PUT request.
  """

  def has_permission(self, request, view):
    return request.method == "PUT"

class IsDeleteRequest(BasePermission):
  """
  Handles permission requests in regards to if a request is a DELETE request.
  """

  def has_permission(self, request, view):
    return request.method == "DELETE"
