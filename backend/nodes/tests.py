from django.urls import reverse
from .models import Node
from .util import get_auth_from_host
from deadlybird.base_test import BaseTestCase
from deadlybird.settings import SITE_REMOTE_AUTH_USERNAME, SITE_REMOTE_AUTH_PASSWORD
import requests
import os
import base64

port = os.environ.get("PORT", "8000")
# Create your tests here.
class NodeTest(BaseTestCase):
  def setUp(self):
    super().setUp()
    self.admin_user = self.create_author(username="admin", password="admin")
    self.test_host = f"http://localhost:{port}/" 
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

  def test_http_basic_auth(self):
    """
    Test that routes that require authorization accept the correct credentials.
    """
    request = self.client.get(reverse("authors"), headers={
       "Authorization": f"Basic {base64.b64encode(bytes(f'{SITE_REMOTE_AUTH_USERNAME}:{SITE_REMOTE_AUTH_PASSWORD}', encoding='utf8')).decode('ascii')}"
    })
    self.assertEquals(request.status_code, 200)