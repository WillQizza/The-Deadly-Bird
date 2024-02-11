from django.test import TestCase
from rest_framework import status

from identity.models import Author
from django.contrib.auth.models import User

# Create your tests here.
class AuthenticationViewsTest(TestCase):
  def setUp(self):
    admin_user = User.objects.create_user(username="admin", password="admin")
    Author.objects.create(
      user=admin_user,
      host="localhost",
      profile_url="localhost"
    )

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