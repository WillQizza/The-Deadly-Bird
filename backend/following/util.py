from .models import Following

def is_friends(author_id: int, other_author_id: int):
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