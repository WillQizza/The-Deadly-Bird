"""
A base test setup which initializes the database with several authors, posts,
followers, inbox messages etc to avoid the redundancy of re-populating the
database for each app's test-suite.
"""

from django.test import TestCase
from identity.models import Author, InboxMessage
from posts.models import Post, Comment
from following.models import Following, FollowingRequest
from django.contrib.auth.models import User
from likes.models import Like

class BaseTestCase(TestCase):

    def setUp(self):
        self.authors            = self.create_authors()
        self.posts              = self.create_posts(self.authors)
        self.follow_requests    = self.create_follow_request(self.authors)
        self.following          = self.create_following(self.authors)
        self.inbox_messages     = self.create_inbox_messages()

    def edit_session(self, **kwargs):
        session = self.client.session
        for prop in kwargs:
            session[prop] = kwargs[prop]
        session.save()

    @staticmethod
    def create_authors():
        """
        Create ten authors
        """
        authors = []
        for i in range(1, 11):
            user = User.objects.create_user(username=f'user{i}', password='password123')
            author = Author.objects.create(user=user, host='http://localhost:8000')
            authors.append(author)
        return authors

    @staticmethod
    def create_posts(authors):
        """
        Create a post for each author
        """
        posts = []
        for i, author in enumerate(authors, start=1):
            post = Post.objects.create(
                title=f"Post {i}",
                description="A sample post.",
                content_type=Post.ContentType.PLAIN,
                content="This is a test post.",
                author=author,
                visibility=Post.Visibility.PUBLIC
            )
            posts.append(post)
        return posts

    @staticmethod
    def create_following(authors):
        """
        Create following relationships
        """
        followings = []
        for i, author in enumerate(authors):
            followed_author = authors[-i]
            if followed_author != author:
                follow = Following.objects.create(author=author, target_author=followed_author)
                followings.append(follow)
        return followings
 
    @staticmethod
    def create_follow_request(authors):
        """
        Create follow requests between authors.
        """
        follow_requests = []
        for i in range(len(authors)):
            target_author = authors[(i + 1) % len(authors)]
            follow_request = FollowingRequest.objects.create(
                author=authors[i],
                target_author=target_author
            )
            follow_requests.append(follow_request)
        return follow_requests

    def create_inbox_messages(self):
        """
        Create inbox messages for posts and follow requests.
        """
        inbox_messages = []
        for post in self.posts:
            msg = InboxMessage.objects.create(
                author=post.author,
                content_id=post.id,
                content_type=InboxMessage.ContentType.POST
            )
            inbox_messages.append(msg)

        for follow_request in self.follow_requests:
            msg = InboxMessage.objects.create(
                author=follow_request.target_author,
                content_id=follow_request.id,
                content_type=InboxMessage.ContentType.FOLLOW
            )
            inbox_messages.append(msg)
        return inbox_messages

    def create_author(self, username=None, password=None):
        """
        Create a new author and add to the list. Can be assured this author has no
        existing follows, posts etc. I.E it is not a foreign key in any existing row.
        """
        i = len(self.authors) + 1
        default_username = username if username is not None else f"user{i}"
        default_password = password if password is not None else f"user{i}"
        
        user = User.objects.create_user(username=default_username, password=default_password)
        author = Author.objects.create(user=user, host='http://localhost:8000')
        self.authors.append(author)

        return author 

    def create_post(self, author_id):
        post = Post.objects.create(
            title=f"Post from {author_id}",
            description="A sample post.",
            content_type=Post.ContentType.PLAIN,
            content="This is a test post.",
            author=Author.objects.get(id=author_id),
            visibility=Post.Visibility.PUBLIC    
        )
        self.posts.append(post)
        return post

    # def create_like(self, author_id, content_id, content_type):

    #     content = None
    #     if content_type == "POST":
    #         content = Post.objects.get(id=content_id)
    #     elif content_type == "COMMENT":
    #         content = Comment.objects.get(id=content_id)

    #     like = Like.objects.create(
    #         author_id=author_id,
    #         content_id=content, 
    #         content_type=content_type
    #     )
    #     self.likes.append(like)
    #     return like