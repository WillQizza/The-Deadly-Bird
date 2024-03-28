from rest_framework import status
from django.urls import reverse
from identity.models import InboxMessage
from deadlybird.base_test import BaseTestCase
from deadlybird.util import generate_full_api_url
import json
from identity.serializers import AuthorSerializer
from django.contrib.auth.models import User
from likes.models import Like

# Create your tests here.
class AuthenticationTest(BaseTestCase):
  def setUp(self):
    super().setUp()
    self.admin_user = self.create_author(username="admin", password="admin")
  
  def test_incomplete_credentials(self):
    # Should return error that we did not supply both the username and password
    response = self.client.post("/api/login/", {
      "username": "admin"
    })
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_login_no_account(self):
    # Should return error that account does not exist
    response = self.client.post("/api/login/", {
      "username": "invalid user",
      "password": "admin"
    })
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_login_wrong_password(self):
    # Should return error that account credentials invalid
    response = self.client.post("/api/login/", {
      "username": "admin",
      "password": "incorrect"
    })
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_login_valid(self):
    # Should be successful
    response = self.client.post("/api/login/", {
      "username": "admin",
      "password": "admin"
    })
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_register_existing_account(self):
    # Should return error since account exists
    response = self.client.post("/api/register/", {
      "username": "admin",
      "password": "admin",
      "email": "admin@admin.com"
    })
    self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

  def test_register_valid(self):
    # Should be successful
    response = self.client.post("/api/register/", {
      "username": "newuser",
      "password": "newuser",
      "email": "newuser@newuser.com"
    })
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Double check that we cannot login without admin apporval
    response = self.client.post("/api/login/", {
      "username": "newuser",
      "password": "newuser"
    })
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    user = User.objects.get(username="newuser")
    user.is_active = True
    user.save()

    # Double check that we can login with the newly created user
    response = self.client.post("/api/login/", {
      "username": "newuser",
      "password": "newuser"
    })
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_register_invalid(self):
    response = self.client.post("/api/register/", {
      "username": "u"*151,
      "password": "newuser",
      "email": "e"*255
    })
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthorTests(BaseTestCase):
  def setUp(self):
    super().setUp()

  def test_retrieving_all_authors(self):
    """
    Check the list of authors retrieved is valid.
    """
    self.edit_session(id=self.authors[0].id)

    # Check that we only extract 5 authors from page 1
    response1 = self.client.get(reverse("authors"), { "size": 5 }).json()
    self.assertEquals(len(response1["items"]), 5)

    # Check that each author object is a valid author
    for author in response1["items"]:
      self.assertTrue(self._is_author_object(author))

    # Check that the second page also has 5 authors
    # (we only created 10)
    response2 = self.client.get(reverse("authors"), { "size": 5, "page": 2 }).json()
    self.assertEquals(len(response2["items"]), 5)

    # Check that each author object is a valid author that was not from response1
    response_1_ids = set(author["id"] for author in response1["items"])
    for author in response2["items"]:
      self.assertTrue(self._is_author_object(author))
      self.assertNotIn(author["id"], response_1_ids)

  def test_retrieving_author(self):
    """
    Check that details are accurate when retrieving a specific author
    """
    self.edit_session(id=self.authors[0].id)

    response = self.client.get(reverse("author", kwargs={ "author_id": self.authors[1].id })).json()
    self.assertEquals(response["id"], generate_full_api_url("author", kwargs={ "author_id": self.authors[1].id }, force_no_slash=True))
    self.assertEquals(response["displayName"], self.authors[1].display_name)

  def _is_author_object(self, obj):
    """
    Check that an author object is valid.
    """
    properties = ["type", "id", "url", "host", "displayName", "github", "profileImage"]
    for property in properties:
      if not property in obj:
        return False
    return True


class InboxMessageTests(BaseTestCase):
  def setUp(self):
    super().setUp()

  def test_inbox_get(self):
    """
    Get the contents of Author0's inbox and make some assertions.
    """
    self.edit_session(id=self.authors[0].id)

    url = reverse('inbox', kwargs={
      "author_id": self.authors[0].id 
    })
    response = self.client.get(url)
    self.assertEquals(response.status_code, 200)
    self.assertTrue(len(response.json()['items']) > 0)

  def test_inbox_post(self):
    """
    Emulate adding sending a random like to Author0's inbox
    """
    self.edit_session(id=self.authors[0].id)

    url = reverse('inbox', kwargs={
      "author_id": self.authors[0].id 
    })
    
    post = self.create_post(self.authors[0].id)

    request_body = {
      "@context": "...",
      "summary": "Summary",
      "type": "Like",
      "author": AuthorSerializer(self.authors[1]).data,
      "object": generate_full_api_url("post", kwargs={ "author_id": post.author.id, "post_id": post.id })
    }
    
    response = self.client.post(url, data=json.dumps(request_body), content_type='application/json')
    self.assertEquals(response.status_code, 201)

  def test_inbox_follow(self):
    """
    Emulate a Follow Request message. 
    """
    self.edit_session(id=self.authors[0].id)

    url = generate_full_api_url('inbox', kwargs={
      "author_id": self.authors[0].id
    })

    target_author = self.create_author()
    author = self.create_author()

    request_body = {
      "summary": "Summary",
      "type": "Follow",
      "actor": AuthorSerializer(author).data,
      "object": AuthorSerializer(target_author).data
    }
    
    response = self.client.post(url, data=json.dumps(request_body), content_type='application/json')
    self.assertEquals(response.status_code, 201)

  def test_inbox_delete(self):
    """
    Get the contents of Author0's delete and assert nothing remains.
    """
    self.edit_session(id=self.authors[0].id)
    
    url = reverse('inbox', kwargs={
      "author_id": self.authors[0].id 
    })
    response = self.client.delete(url)
    self.assertEquals(response.status_code, 204)
    msgs = InboxMessage.objects.filter(author_id=self.authors[0].id)
    self.assertTrue(len(msgs) == 0)