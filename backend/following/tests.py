"""
- Tests.py
- Justin Meimar

Run tests for the Following and FollowRequest models and views
"""

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from identity.models import Author
from .models import Following, FollowingRequest
from typing import List

class FollowersTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.authors = self.create_authors()

    @staticmethod
    def create_authors() -> List[Author]:
        authors = []
        for i in range(1, 4):
            user = User.objects.create_user(username=f'user{i}', password='password123')
            author = Author.objects.create(user=user, host='http://localhost:8000')
            authors.append(author)
        return authors

    def test_create_following(self):
        author1, author2, author3 = self.authors
        Following.objects.create(author=author1, target_author=author2)
        Following.objects.create(author=author1, target_author=author3)

        self.assertEqual(Following.objects.filter(author=author1).count(), 2)
        self.assertTrue(Following.objects.filter(author=author1, target_author=author2).exists())
        self.assertTrue(Following.objects.filter(author=author1, target_author=author3).exists())

    def test_get_followers(self):
        self.test_create_following()
        
        author2 = self.authors[1]
        url = reverse('followers', kwargs={'author_id': author2.user.id})
        response = self.client.get(url)
        
        self.assertTrue(len(response.json()['results']['items']) == 1)
        self.assertTrue(response.json()['results']['items'][0]['id'] == 1);
        self.assertEqual(response.status_code, 200)

    def test_delete_follower(self):
        author1, author2, _ = self.authors
        Following.objects.create(author=author2, target_author=author1)
        self.assertTrue(Following.objects.filter(author=author2, target_author=author1).exists())
        response = self.client.delete(reverse('modify_follower', kwargs={
            'author_id': author1.id, 'foreign_author_id': author2.id
            }))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Following.objects.filter(author=author2, target_author=author1).exists())

    def test_put_follower(self):
        author1, author2, _ = self.authors
        response = self.client.put(reverse('modify_follower', kwargs={
            'author_id': author1.id, 'foreign_author_id': author2.id
            }))
        self.assertIn(response.status_code, [201, 200])
        self.assertTrue(Following.objects.filter(author=author2, target_author=author1).exists())

    def test_get_follower_exists(self):
        author1, author2, _ = self.authors
        Following.objects.create(author=author2, target_author=author1)
        response = self.client.get(reverse('modify_follower', kwargs={
            'author_id': author1.id, 'foreign_author_id': author2.id
            }))
        self.assertEqual(response.status_code, 200)

    def test_get_follower_not_exists(self):
        author1, author2, _ = self.authors
        response = self.client.get(reverse('modify_follower', kwargs={
            'author_id': author1.id, 'foreign_author_id': author2.id
            }))
        self.assertEqual(response.status_code, 404)

    def test_follow_requests(self):
        author1, author2, _ = self.authors

        # Create a following request from author1 to author2
        follow_reqs = FollowingRequest.objects.filter()
        self.assertTrue(len(follow_reqs) == 0)

        url = reverse('request_follower', kwargs={
            'local_author_id': author1.id, 'foreign_author_id': author2.id
        })
        self.client.post(url)
        follow_req_obj = FollowingRequest.objects.filter(target_author=author2.id, author=author1.id) 
        self.assertTrue(follow_req_obj is not None)

        # Test sending the same request, while it is already outstanding
        response = self.client.post(url)
        self.assertEqual(response.status_code, 409)


    def test_follow_request_to_existing_follow(self):

        author1, author2, _ = self.authors
        self.test_create_following()

        url = reverse('request_follower', kwargs={
            'local_author_id': author1.id, 'foreign_author_id': author2.id
        })
        self.client.post(url)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 409)