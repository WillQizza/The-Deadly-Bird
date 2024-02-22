import secrets

def generate_next_id():
  return secrets.token_urlsafe(10)