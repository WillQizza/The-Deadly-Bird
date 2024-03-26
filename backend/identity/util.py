from .models import Author
from django.http import HttpRequest
from deadlybird.settings import SITE_HOST_URL
from deadlybird.util import compare_domains

def get_this_host_url() -> str:
    """
    Gets the url of this host
    """
    return SITE_HOST_URL.rstrip("/")

def check_authors_exist(*author_ids: int) -> bool:
    """
    Checks if authors passed as comma separated parameters all exist 
    """
    for author_id in author_ids:
        if not Author.objects.filter(id=author_id).exists():
            return False
    return True

def check_author_is_remote(author_id: str) -> bool:
    """
    Checks if an author is from a remote host
    """
    this_host = get_this_host_url()
    author = Author.objects.filter(id=author_id).first()
    if author is not None: 
        check_host = author.host
        # if hosts don't match then remote author
        return not compare_domains(this_host, check_host)
    # author does not exist 
    return False