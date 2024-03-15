from .models import Node

def get_auth_from_host(host):
    "Given host return the authentication tuple"
    try:
        node = Node.objects.all()\
            .filter(host=host)\
            .first()

        return (node.outgoing_username, node.outgoing_password) 
    except:
        return (None, None)