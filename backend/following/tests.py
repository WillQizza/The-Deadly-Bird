"""
- Tests.py
- Justin Meimar

Run tests for the Following and FollowRequest models and views
"""

from django.urls import reverse
from .models import Following, FollowingRequest
from deadlybird.base_test import BaseTestCase
from identity.models import InboxMessage

class FollowersTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_get_followers(self):
        
        author2 = self.authors[1]
        self.edit_session(id=author2.id)

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

        self.edit_session(id=author1.id)

        self.assertTrue(Following.objects.filter(author=author2, target_author=author1).exists())
        response = self.client.delete(reverse('modify_follower', kwargs={
            'author_id': author1.id, 'foreign_author_id': author2.id
            }))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Following.objects.filter(author=author2, target_author=author1).exists())

    def test_put_follower(self):
        
        author1 = self.create_author() 
        author2 = self.create_author() 

        self.edit_session(id=author1.id)
        
        response = self.client.put(reverse('modify_follower', kwargs={
            'author_id': author1.id, 'foreign_author_id': author2.id
            }))
        self.assertIn(response.status_code, [409, 201])
        self.assertTrue(Following.objects.filter(author=author2, target_author=author1).exists())


    def test_get_follower_exists(self):
        existing_follow = self.following[0]
        author1 = existing_follow.author
        author2 = existing_follow.target_author

        self.edit_session(id=author1.id)
        
        response = self.client.get(reverse('modify_follower', kwargs={
            'author_id': author1.id, 'foreign_author_id': author2.id
            }))
        self.assertEqual(response.status_code, 200)

    def test_get_follower_not_exists(self):
        
        author1 = self.create_author()
        author2 = self.create_author()

        self.edit_session(id=author1.id)

        response = self.client.get(reverse('modify_follower', kwargs={
            'author_id': author1.id, 'foreign_author_id': author2.id
            }))
        self.assertEqual(response.status_code, 404)

    def test_following_request_get(self):
        req : FollowingRequest = self.follow_requests[0] 
        from_author_id = req.author.id
        to_author_id = req.target_author.id

        self.edit_session(id=from_author_id)

        url = reverse('request_follower', kwargs={
            'local_author_id': from_author_id, 
            'foreign_author_id': to_author_id
        })
        
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)