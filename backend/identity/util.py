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