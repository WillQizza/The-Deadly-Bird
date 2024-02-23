from django.test import TestCase
from deadlybird.base_test import BaseTestCase
from .models import Like
from django.urls import reverse

class LikeTests(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_likes(self):
        self.create_likes()
        likes = Like.objects.filter()
        
        a1, a2, a3 = (self.authors[0], self.authors[1], self.authors[2])
        url = reverse('post_likes', kwargs={
            'author_id': a2.id,
            'post_id': '1'
        })
         
        res = self.client.get(url)
        self.assertTrue(res.status_code == 404)

        url = reverse('post_likes', kwargs={
            'author_id': '1',
            'post_id': '1'
        })
        print(res.json())
        print(likes)

    def create_likes(self):
        a1, a2, a3 = (self.authors[0], self.authors[1], self.authors[2])
        post = self.create_post(a1.id)

        # a2 likes a1 post
        Like.objects.create(
            author_id=a2.id,
            content_id=post.id,
            content_type=Like.ContentType.POST
        )

        # a3 likes a1 post
        Like.objects.create(
            author_id=a3.id,
            content_id=post.id,
            content_type=Like.ContentType.POST
        ) 