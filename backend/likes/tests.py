from django.test import TestCase
from deadlybird.base_test import BaseTestCase
from .models import Like
from posts.models import Post
from django.urls import reverse

class LikeTests(BaseTestCase):
    def setUp(self):
        super().setUp()
    
    def test_likes_posts(self):
        a1, a2 = (self.authors[0], self.authors[1])
        post = Post.objects.filter(author=a1).order_by("published_date").first()
        
        # successful query; a1 has a post called post_id, but no likes on it
        url = reverse('post_likes', kwargs={
            'author_id': a1.id,
            'post_id': post.id
        })
        json = self.client.get(url).json()
        self.assertTrue(len(json) == 0)

        self.create_likes()  

        # successful query; a1 has a post with post.id 
        json = self.client.get(url).json()
        self.assertTrue(len(json) == 2)

        # author_id does not correspond to post_id, but post_id exists
        url = reverse('post_likes', kwargs={
            'author_id': a2.id,
            'post_id': post.id
        })
        json = self.client.get(url).json()
        self.assertTrue(json['message'] is not None)

    def test_liked(self):
        a1, a2 = (self.authors[0], self.authors[1])
        
        self.create_likes()  
        # successful query; a1 has a post called post_id, but no likes on it
        url = reverse('liked', kwargs={
            'author_id': a2.id,
        })
        json = self.client.get(url).json()
        self.assertTrue(len(json['items']) == 1)

    def create_comments(self):
        #TODO: test likes on comments
        pass

    def create_likes(self):
        a1, a2, a3 = (self.authors[0], self.authors[1], self.authors[2])
        
        post = Post.objects.filter(author=a1).order_by("published_date").first() 

        # a2 likes a1 post
        Like.objects.create(
            send_author_id=a2.id,
            receive_author_id=a1.id,
            content_id=post.id,
            content_type=Like.ContentType.POST
        )

        # a3 likes a1 post
        Like.objects.create(
            send_author_id=a3.id,
            receive_author_id=a1.id,
            content_id=post.id,
            content_type=Like.ContentType.POST
        ) 