import base64
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

class RemoteNodeAuthentication(BaseAuthentication):
  """
  Handles remote node authentication request handling
  Remote nodes must send the "Authorization" header with "Basic base64_of_username:password"
  """

  def authenticate(self, request):
    auth_parts = get_authorization_header(request).split()
    request.is_node_authenticated = False

    # Only allow basic authentication
    if not auth_parts or auth_parts[0].lower() != b"basic":
      print("no header detected")
      return None
    
    # Authentication headers should only be 2 parts. "Basic base64StringHere"
    if len(auth_parts) != 2:
      print("no structure")
      raise exceptions.ParseError("Invalid Authorization header: invalid structure")
    
    b64_str = auth_parts[1]
    try:
      decoded_b64 = base64.b64decode(b64_str).decode("utf-8")
    except:
      # Invalid b64
      print("invalid base64")
      raise exceptions.ParseError("Invalid Authorization header: invalid base64")
    
    # Ensure encoded credentials is correct format
    credentials_arr = decoded_b64.split(":")
    if len(credentials_arr) != 2:
      print("invalid creds")
      raise exceptions.ParseError("Invalid Authorization header: invalid credentials format")
    
    username, password = credentials_arr

    if (username != settings.SITE_REMOTE_AUTH_USERNAME) \
      or (password != settings.SITE_REMOTE_AUTH_PASSWORD):
        print("wrong password")
        print(f"received ({username}, {password}) when I was expecting ({settings.SITE_REMOTE_AUTH_USERNAME}, {settings.SITE_REMOTE_AUTH_PASSWORD})")
        raise exceptions.NotAuthenticated("Invalid Authorization header: Invalid credentials")

    print("request authorized")
    request.is_node_authenticated = True
    return (None, None)

  def authenticate_header(self, request):
    return "Basic realm=\"api\""