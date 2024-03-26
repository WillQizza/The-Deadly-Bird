from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from deadlybird.permissions import RemoteOrSessionAuthenticated
from deadlybird.settings import SITE_HOST_URL

@api_view(["GET"])
@permission_classes([RemoteOrSessionAuthenticated])
def _getHostname(request: HttpRequest):
  """
  private method used by frontend to get the hostname for distinguishing between local
  and remote authors
  """
  return Response({"hostname": SITE_HOST_URL}, status=200) 