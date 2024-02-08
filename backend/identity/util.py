from typing import Union
from .models import Author
from django.http import HttpRequest
from rest_framework.response import Response

def check_authors_exist(*author_ids: int) -> bool:
    """
    Checks if authors passed as comma separated parameters all exist 
    """
    for author_id in author_ids:
        if not Author.objects.filter(id=author_id).exists():
            return False
    return True

def validate_login_session(request: HttpRequest) -> Union[bool, Response]:
    """
    Validate a login session, return a forbidden response if unauthenticated, otherwise True 
    """
    try:
        author_id = request.session.get("id")
        if author_id and check_authors_exist(author_id):
            return True
        else:
            return Response({
                "message": "Forbidden: Unauthorized request or session expired."
            }, status=403)
    except KeyError:
        return Response({
            "message": "Forbidden: Unauthorized request."
        }, status=403) 