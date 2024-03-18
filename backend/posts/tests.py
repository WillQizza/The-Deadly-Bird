from django.urls import reverse
from deadlybird.base_test import BaseTestCase
from deadlybird.util import generate_full_api_url
from following.models import Following
from .models import Comment, Post

# Create your tests here.

class AuthorPostTest(BaseTestCase):
  def setUp(self):
    return super().setUp()
  
  def test_getting_public_posts(self):
    """
    Check the list of posts retrieved is valid.
    """
    self.edit_session(id=self.authors[0].id)

    Post.objects.create(
        title=f"Another Post",
        description="A sample post.",
        content_type=Post.ContentType.PLAIN,
        content="This is a test post.",
        author=self.authors[0],
        visibility=Post.Visibility.PUBLIC,
        source=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" }),
        origin=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" })
    )

    # Check that we only extract 5 posts from page 1
    response1 = self.client.get(reverse("posts", kwargs={ "author_id": self.authors[0].id }), { "size": 1 }).json()
    self.assertEquals(len(response1["items"]), 1)

    # Check that each post object is a valid post
    for post in response1["items"]:
      self.assertTrue(self._is_post_object(post))

    # Check that the second page also has 5 posts
    response2 = self.client.get(reverse("posts", kwargs={ "author_id": self.authors[0].id }), { "size": 1, "page": 2 }).json()
    self.assertEquals(len(response2["items"]), 1)

    # Check that each post object is a valid post that was not from response1
    response_1_ids = set(post["id"] for post in response1["items"])
    for post in response2["items"]:
      self.assertTrue(self._is_post_object(post))
      self.assertNotIn(post["id"], response_1_ids)

  def test_getting_friend_posts(self):
    """
    Check that friends posts are only shown to friends or ourselves.
    """
    self.edit_session(id=self.authors[1].id)

    # Create a friend post
    Post.objects.create(
        title=f"FRIEND",
        description="A sample post.",
        content_type=Post.ContentType.PLAIN,
        content="This is a test post.",
        author=self.authors[0],
        visibility=Post.Visibility.FRIENDS,
        source=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" }),
        origin=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" })
    )

    # Should not have the friend post
    response = self.client.get(reverse("posts", kwargs={ "author_id": self.authors[0].id }), { "size": 100 }).json()
    for post in response["items"]:
      self.assertNotEqual(post["visibility"], "FRIENDS")

    # Should now have the friend post
    Following.objects.create(
      author=self.authors[0],
      target_author=self.authors[1]
    )
    Following.objects.create(
      author=self.authors[1],
      target_author=self.authors[0]
    )
    self.edit_session(id=self.authors[1].id)
    response = self.client.get(reverse("posts", kwargs={ "author_id": self.authors[0].id }), { "size": 100 }).json()

    found_friends_visibility = next((True for post in response["items"] if post["visibility"] == "FRIENDS"), False)
    self.assertTrue(found_friends_visibility)

  def test_getting_unlisted_posts(self):
    """
    Check that unlisted posts are not publicly listed unless it is from us.
    """
    self.edit_session(id=self.authors[1].id)

    # Create a unlisted post
    Post.objects.create(
        title=f"UNLISTED",
        description="A sample post.",
        content_type=Post.ContentType.PLAIN,
        content="This is a test post.",
        author=self.authors[0],
        visibility=Post.Visibility.UNLISTED,
        source=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" }),
        origin=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" })
    )

    # Should not have the unlisted post
    response = self.client.get(reverse("posts", kwargs={ "author_id": self.authors[0].id }), { "size": 100 }).json()
    for post in response["items"]:
      self.assertNotEqual(post["visibility"], "UNLISTED")

    # Should now have the unlisted post
    self.edit_session(id=self.authors[0].id)
    response = self.client.get(reverse("posts", kwargs={ "author_id": self.authors[0].id }), { "size": 100 }).json()
    
    found_unlisted_visibility = next((True for post in response["items"] if post["visibility"] == "UNLISTED"), False)
    self.assertTrue(found_unlisted_visibility)

  def test_getting_single_public_post(self):
    """
    Checks that a specific post can be accessed and is valid.
    """
    self.edit_session(id=self.authors[1].id)

    post = Post.objects.create(
        title=f"Another Post",
        description="A sample post.",
        content_type=Post.ContentType.PLAIN,
        content="This is a test post.",
        author=self.authors[0],
        visibility=Post.Visibility.PUBLIC,
        source=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" }),
        origin=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" })
    )

    # Check that we got the post we made
    response1 = self.client.get(reverse("post", kwargs={"post_id": post.id , "author_id": self.authors[0].id }), { "size": 1 }).json()
    self.assertEquals(post.id, response1["id"])
    self.assertEquals(post.author.id, response1["author"]["id"])
    self.assertTrue(self._is_post_object(response1))

  def test_getting_single_friend_post(self):
    """
    Check that a specific post can't be accessed when not friend, but is otherwise valid.
    """
    self.edit_session(id=self.authors[1].id)

    post = Post.objects.create(
        title=f"Another Post",
        description="A sample post.",
        content_type=Post.ContentType.PLAIN,
        content="This is a test post.",
        author=self.authors[0],
        visibility=Post.Visibility.FRIENDS,
        source=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" }),
        origin=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" })
    )

    # Check that we got the post we made
    response1 = self.client.get(reverse("post", kwargs={"post_id": post.id , "author_id": self.authors[0].id }), { "size": 1 }).json()
    self.assertEquals(response1["error"], True)

    # Should now have the friend post
    Following.objects.create(
      author=self.authors[0],
      target_author=self.authors[1]
    )
    Following.objects.create(
      author=self.authors[1],
      target_author=self.authors[0]
    )
    self.edit_session(id=self.authors[1].id)
    response2 = self.client.get(reverse("post", kwargs={"post_id": post.id , "author_id": self.authors[0].id }), { "size": 1 }).json()
    self.assertEquals(post.id, response2["id"])
    self.assertEquals(post.author.id, response2["author"]["id"])
    self.assertTrue(self._is_post_object(response2))

  def test_getting_single_unlisted_post(self):
    """
    Check that a specific unlisted post can be accessed and is valid.
    """
    self.edit_session(id=self.authors[0].id)

    post = Post.objects.create(
        title=f"Another Post",
        description="A sample post.",
        content_type=Post.ContentType.PLAIN,
        content="This is a test post.",
        author=self.authors[0],
        visibility=Post.Visibility.UNLISTED,
        source=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" }),
        origin=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" })
    )

    # Check that we got the post we made
    response1 = self.client.get(reverse("post", kwargs={"post_id": post.id , "author_id": self.authors[0].id }), { "size": 1 }).json()
    self.assertEquals(post.id, response1["id"])
    self.assertEquals(post.author.id, response1["author"]["id"])
    self.assertTrue(self._is_post_object(response1))

  def _is_post_object(self, obj):
    """
    Assert that the JSON post object provided matches the API spec.
    """
    properties = ["type", "title", "id", "source", "origin", "description", "contentType", 
                  "content", "author", "count", "comments", "commentsSrc", "published", 
                  "visibility"]
    for property in properties:
      if not property in obj:
        return False
    return True

  def test_invalid_post_payload(self):
    """
    Check that not providing all valid post form properties is handled.
    """
    self.edit_session(id=self.authors[0].id)
    response = self.client.post(reverse("posts", kwargs={ "author_id": 1 }))
    self.assertEquals(response.status_code, 400)
  
  def test_invalid_length_post_payload(self):
    """
    Check that providing post form properties with invalid lengths is handled.
    """
    self.edit_session(id=self.authors[0].id)
    response = self.client.post(reverse("posts", kwargs={ "author_id": self.authors[1].id }), {
      "title": "t"*256,
      "description": "d"*256,
      "contentType": "text/plain",
      "content": "Hello World",
      "visibility": Post.Visibility.PUBLIC
    })
    self.assertEquals(response.status_code, 400)

  def test_impersonation_post_payload(self):
    """
    Check that we cannot create a post as someone else we are not.
    """
    self.edit_session(id=self.authors[0].id)
    response = self.client.post(reverse("posts", kwargs={ "author_id": self.authors[1].id }), {
      "title": "Post",
      "description": "Desc",
      "contentType": "text/plain",
      "content": "Hello World",
      "visibility": Post.Visibility.PUBLIC
    })
    self.assertEquals(response.status_code, 401)

  def test_valid_post_payload(self):
    """
    Check that we can create a post.
    """
    self.edit_session(id=self.authors[0].id)
    response = self.client.post(reverse("posts", kwargs={ "author_id": self.authors[0].id }), {
      "title": "Post",
      "description": "Desc",
      "contentType": "text/plain",
      "content": "Hello World",
      "visibility": Post.Visibility.PUBLIC
    })
    self.assertEquals(response.status_code, 201)

    post_exists = Post.objects.all().filter(title="Post").exists()
    self.assertTrue(post_exists)

  def test_delete_post(self):
    """
    Test delete on 1) non existent post and 2) existing post.
    """ 
    a1 = self.create_author()
    self.edit_session(id=a1.id)

    payload = {
      "post_id": "non-existent-id",
      "author_id": a1.id
    }
    res = self.client.delete(reverse("post", kwargs=payload))
    self.assertTrue(res.status_code == 404)
    
    post = self.create_post(a1.id)
    payload = {
      "post_id": post.id,
      "author_id": a1.id
    }
    res = self.client.delete(reverse("post", kwargs=payload)) 
    self.assertTrue(res.status_code == 204)
  
  def _is_comment_object(self, obj):
    """
    Assert that the JSON comment object provided matches the API spec.
    """
    properties = ["type", "author", "comment", "contentType", "published", 
                  "id"]
    for property in properties:
      if not property in obj:
        return False
    return True
  
  def test_getting_post_comments(self):
    """
    Check the list of comments retrieved for a post is valid.
    """
    self.edit_session(id=self.authors[0].id)

    # Create comments on a post
    post = Post.objects.create(
        title=f"Sample Post",
        description="A sample post.",
        content_type=Post.ContentType.PLAIN,
        content="This is a test post.",
        author=self.authors[0],
        visibility=Post.Visibility.PUBLIC,
        source=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" }),
        origin=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" })
    )

    Comment.objects.create(
      post=post,
      author=self.authors[1],
      content="This is the first test comment.",
      content_type=Comment.ContentType.PLAIN
    )

    Comment.objects.create(
      post=post,
      author=self.authors[0],
      content="This is the second test comment.",
      content_type=Comment.ContentType.MARKDOWN
    )

    # Check that the number of comments on each page is correct
    response1 = self.client.get(reverse("comments", kwargs={ "post_id": post.id, "author_id": self.authors[0].id }), { "size": 1, "page": 1 }).json()
    response2 = self.client.get(reverse("comments", kwargs={ "post_id": post.id, "author_id": self.authors[0].id }), { "size": 1, "page": 2 }).json()
    self.assertEquals(len(response1["comments"]), 1)
    self.assertEquals(len(response2["comments"]), 1)

    # Check that each comment object is a valid comment
    self.assertTrue(self._is_comment_object(response1["comments"][0]))
    self.assertTrue(self._is_comment_object(response2["comments"][0]))
  
  def test_getting_comments_nopost(self):
    """
    Check that we handle trying to get comments for a post that does not exist.
    """
    self.edit_session(id=self.authors[0].id)
    response = self.client.get(reverse("comments", kwargs={ "author_id": self.authors[0].id, "post_id": "random_nonexistent_post_id" }))
    self.assertEquals(response.status_code, 404)

  def test_invalid_comment_payload(self):
    """
    Check that not providing all valid comment form properties is handled.
    """
    self.edit_session(id=self.authors[0].id)
    post = Post.objects.create(
        title=f"Sample Post",
        description="A sample post.",
        content_type=Post.ContentType.PLAIN,
        content="This is a test post.",
        author=self.authors[0],
        visibility=Post.Visibility.PUBLIC,
        source=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" }),
        origin=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" })
    )
    response = self.client.post(reverse("comments", kwargs={ "author_id": self.authors[0].id, "post_id": post.id }))
    self.assertEquals(response.status_code, 400)
  
  def test_invalid_comment_body_payload(self):
    """
    Check that providing comment form properties with invalid values is handled.
    """
    self.edit_session(id=self.authors[0].id)
    post = Post.objects.create(
        title=f"Sample Post",
        description="A sample post.",
        content_type=Post.ContentType.PLAIN,
        content="This is a test post.",
        author=self.authors[0],
        visibility=Post.Visibility.PUBLIC,
        source=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" }),
        origin=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" })
    )
    response = self.client.post(reverse("comments", kwargs={ "author_id": self.authors[0].id, "post_id": post.id }), {
      "contentType": "text/",
      "comment": ""
    })
    self.assertEquals(response.status_code, 400)

  def test_valid_comment_payload(self):
    """
    Check that we can comment on a post.
    """
    self.edit_session(id=self.authors[1].id)
    post = Post.objects.create(
        title=f"Sample Post",
        description="A sample post.",
        content_type=Post.ContentType.PLAIN,
        content="This is a test post.",
        author=self.authors[0],
        visibility=Post.Visibility.PUBLIC,
        source=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" }),
        origin=generate_full_api_url("post", kwargs={ "author_id": "a", "post_id": "a" })
    )
    response = self.client.post(reverse("comments", kwargs={ "author_id": self.authors[0].id, "post_id": post.id }), {
      "contentType": "text/plain",
      "comment": "Hello World"
    })
    self.assertEquals(response.status_code, 201)

    comment_exists = Comment.objects.all().filter(content="Hello World").exists()
    self.assertTrue(comment_exists)
  
  def test_getting_comments_nopost(self):
    """
    Check that we cannot comment on a post that does not exist.
    """
    self.edit_session(id=self.authors[0].id)
    response = self.client.post(reverse("comments", kwargs={ "author_id": self.authors[0].id, "post_id": "random_nonexistent_post_id" }), {
      "contentType": "text/plain",
      "comment": "Hello World"
    })
    self.assertEquals(response.status_code, 404)