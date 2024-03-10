from .models import Author
from django.http import HttpRequest

def check_authors_exist(*author_ids: int) -> bool:
    """
    Checks if authors passed as comma separated parameters all exist 
    """
    for author_id in author_ids:
        if not Author.objects.filter(id=author_id).exists():
            return False
    return True

def validate_login_session(request: HttpRequest) -> bool:
    """
    Validate a login session, return True if the session is valid.
    """
    try:
        author_id = request.session.get("id")
        if author_id and check_authors_exist(author_id):
            return True
        else:
            return False
    except KeyError:
        return False