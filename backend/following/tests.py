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
from deadlybird.base_test import BaseTestCase
from identity.models import InboxMessage

class FollowersTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_get_followers(self):
        
        author2 = self.authors[1]
        url = reverse('followers', kwargs={'author_id': author2.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_following(self):

        author1 = self.create_author()
        author2 = self.create_author()
        author3 = self.create_author()

        Following.objects.create(author=author1, target_author=author2)
        Following.objects.create(author=author1, target_author=author3)

        self.assertEqual(Following.objects.filter(author=author1).count(), 2)
        self.assertTrue(Following.objects.filter(author=author1, target_author=author2).exists())
        self.assertTrue(Following.objects.filter(author=author1, target_author=author3).exists())

    def test_delete_follower(self):
        
        existing_follow = self.following[0]
        author1 = existing_follow.author
        author2 = existing_follow.target_author

        self.assertTrue(Following.objects.filter(author=author2, target_author=author1).exists())
        response = self.client.delete(reverse('modify_follower', kwargs={
            'author_id': author1.id, 'foreign_author_id': author2.id
            }))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Following.objects.filter(author=author2, target_author=author1).exists())

    def test_put_follower(self):
        
        author1 = self.create_author() 
        author2 = self.create_author() 
        
        response = self.client.put(reverse('modify_follower', kwargs={
            'author_id': author1.id, 'foreign_author_id': author2.id
            }))
        self.assertIn(response.status_code, [201, 200])
        self.assertTrue(Following.objects.filter(author=author2, target_author=author1).exists())


    def test_get_follower_exists(self):
        existing_follow = self.following[0]
        author1 = existing_follow.author
        author2 = existing_follow.target_author
        
        response = self.client.get(reverse('modify_follower', kwargs={
            'author_id': author1.id, 'foreign_author_id': author2.id
            }))
        self.assertEqual(response.status_code, 200)

    def test_get_follower_not_exists(self):
        
        author1 = self.create_author()
        author2 = self.create_author()

        response = self.client.get(reverse('modify_follower', kwargs={
            'author_id': author1.id, 'foreign_author_id': author2.id
            }))
        self.assertEqual(response.status_code, 404)

    def test_follow_requests(self):
        author1 = self.create_author()
        author2 = self.create_author()

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

        existing_follow = self.following[0]
        author1 = existing_follow.author
        author2 = existing_follow.target_author
        
        url = reverse('request_follower', kwargs={
            'local_author_id': author1.id, 'foreign_author_id': author2.id
        })
        self.client.post(url)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 409)

    def test_follow_request_inbox_redirect(self):

        author1 = self.create_author()
        author2 = self.create_author()

        url = reverse('request_follower', kwargs={
            'local_author_id': author1.id, 'foreign_author_id': author2.id
        })
        
        follow_reqs = FollowingRequest.objects.filter(
            author=author1.id,
            target_author=author2.id
        )

        self.assertTrue(len(follow_reqs) == 0)  
        response = self.client.post(url)
        self.assertTrue(response.status_code == 201)
        
        
        follow_req = FollowingRequest.objects.filter(
            author=author1.id,
            target_author=author2.id
        ).first()

        self.assertTrue(follow_req is not None)  

        inbox_message = InboxMessage.objects.filter(
            author=author2.id,
            content_id=follow_req.id
        ).first()

        self.assertTrue(inbox_message is not None)

    def test_following_api(self):

        author2 = self.authors[1]
        url = reverse('following', kwargs={'author_id': author2.user.id})
        following = self.client.get(url)
        self.assertTrue(following.json()['count'] > 0)

        include_author_ids = '1,2,3'
        response = self.client.get(url, data={'include_author_ids': include_author_ids}) 
        self.assertTrue(response.json()['count'] == 0)