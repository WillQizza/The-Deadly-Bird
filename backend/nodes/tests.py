from .models import Node
from .util import get_auth_from_host
from deadlybird.base_test import BaseTestCase
import requests
import os

port = os.environ.get("PORT", "8000")
# Create your tests here.
class NodeTest(BaseTestCase):
  def setUp(self):
    super().setUp()
    self.admin_user = self.create_author(username="admin", password="admin")
    self.test_host = f"http://localhost:{port}/api" 
  def test_add_node(self):
    """
    Verify adding a node works
    """
    try:
        Node.objects.create(
        host=self.test_host, 
        outgoing_username="username",
        outgoing_password="password"
        )
    except Exception as e:
        pass

    qs = Node.objects.all()
    self.assertTrue(len(qs) != 0)

  def test_util(self):
    """
    Verify utility function
    """
    self.test_add_node() 
    auth = get_auth_from_host(self.test_host)
    self.assertTrue(auth is not None \
                    and auth[0] is not None \
                    and auth[1] is not None)
