from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from identity.models import Author, InboxMessage
from django.contrib.auth.models import User
from typing import List
from deadlybird.base_test import BaseTestCase
import json

# Create your tests here.
class AuthenticationViewsTest(BaseTestCase):
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
      "password": "admin"
    })
    self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

  def test_register_valid(self):
    # Should be successful
    response = self.client.post("/api/register/", {
      "username": "newuser",
      "password": "newuser"
    })
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Double check that we can login with the newly created user
    response = self.client.post("/api/login/", {
      "username": "newuser",
      "password": "newuser"
    })
    self.assertEqual(response.status_code, status.HTTP_200_OK)


class InboxMessageTests(BaseTestCase):
  def setUp(self):
    super().setUp()

  def test_inbox_get(self):
    """
    Get the contents of Author0's inbox and make some assertions.
    """
    url = reverse('inbox', kwargs={
      "author_id": self.authors[0].id 
    })
    response = self.client.get(url)
    self.assertEquals(response.status_code, 200)

  def test_inbox_post(self):
    """
    Emulate adding sending a random post to Author0's inbox
    """
    url = reverse('inbox', kwargs={
      "author_id": self.authors[0].id 
    })
    post = self.posts[0]
    request_body = {
      "content_type": InboxMessage.ContentType.POST,
      "content_id": post.id
    }
    
    response = self.client.post(url, data=json.dumps(request_body), content_type='application/json')
    self.assertEquals(response.status_code, 201)