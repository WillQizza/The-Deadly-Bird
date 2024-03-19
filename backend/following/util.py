from .models import Following
from urllib.parse import urlparse

def is_friends(author_id: str, other_author_id: str):
  """
    If two authors are friends, then they should both be following one another.

    Params:
    - author_id - author id A
    - other_author_id - author id B
  """
  try:
    Following.objects.get(author=author_id, target_author=other_author_id)
    Following.objects.get(author=other_author_id, target_author=author_id)
  except Following.DoesNotExist:
    return False

  return True

def compare_domains(url1, url2):
    """
    Compares the domain and port of two URLs to determine if they are equal.
    """
    parsed_url_1 = urlparse(url1)
    parsed_url_2 = urlparse(url2)

    domain1, port1 = (parsed_url_1.hostname, parsed_url_1.port)
    domain2, port2 = (parsed_url_2.hostname, parsed_url_2.port) 

    if port1 and port2:
      return domain1 == domain2 and port1 == port2
    else: 
      return domain1 == domain2