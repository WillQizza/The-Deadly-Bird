from .models import Node

def get_auth_from_host(host):
    "Given host return the authentication tuple"
    node = Node.objects.all()\
        .filter(host=host)\
        .first()

    if node is not None:
        return (node.outgoing_username, node.outgoing_password) 
    else:
        return ('username', 'password')