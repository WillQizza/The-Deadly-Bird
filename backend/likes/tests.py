from django.test import TestCase
from deadlybird.base_test import BaseTestCase
from .models import Like
from posts.models import Post
from django.urls import reverse

class LikeTests(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_likes(self):
         
        self.create_likes()
        a1, a2, a3 = (self.authors[0], self.authors[1], self.authors[2])
        post = Post.objects.filter(author=a1).first() 

        url = reverse('post_likes', kwargs={
            'author_id': a2.id,
            'post_id': post.id
        })
        res = self.client.get(url)
        print(res.json()) 

    def create_likes(self):
        a1, a2, a3 = (self.authors[0], self.authors[1], self.authors[2])
        
        post = Post.objects.filter(author=a1).first() 
        print(post)

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