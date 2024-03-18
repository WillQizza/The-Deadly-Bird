from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from deadlybird.permissions import SessionAuthenticated, RemoteOrSessionAuthenticated
import os

@api_view(["GET"])
@permission_classes([RemoteOrSessionAuthenticated])
def _getHostname(request: HttpRequest):
  """
  private method used by frontend to get the hostname for distinguishing between local
  and remote authors
  """
  hostname = os.environ.get("HOST_URL")
  return Response({"hostname": hostname}, status=200) 