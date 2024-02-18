from django.urls import reverse
from deadlybird.base_test import BaseTestCase
from .models import Post

# Create your tests here.

class AuthorPostTest(BaseTestCase):
  def setUp(self):
    return super().setUp()
  
  def test_getting_public_posts(self):
    """
    Check the list of posts retrieved is valid.
    """
    Post.objects.create(
        title=f"Another Post",
        description="A sample post.",
        content_type=Post.ContentType.PLAIN,
        content="This is a test post.",
        author=self.authors[0],
        visibility=Post.Visibility.PUBLIC
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
    # Create a friend post
    Post.objects.create(
        title=f"FRIEND",
        description="A sample post.",
        content_type=Post.ContentType.PLAIN,
        content="This is a test post.",
        author=self.authors[0],
        visibility=Post.Visibility.UNLISTED
    )

    # Should not have the friend post
    response = self.client.get(reverse("posts", kwargs={ "author_id": self.authors[0].id }), { "size": 100 }).json()
    for post in response["items"]:
      self.assertNotEqual(post["visibility"], "UNLISTED")

    # Should now have the friend post
    self.client.session["id"] = self.authors[1].id
    response = self.client.get(reverse("posts", kwargs={ "author_id": self.authors[0].id }), { "size": 100 }).json()

    found_friends_visibility = next((True for post in response["items"] if post["visibility"] == "FRIENDS"), False)
    self.assertTrue(found_friends_visibility)

    # TODO: Check again but with our user id


  def test_getting_unlisted_posts(self):
    # Create a unlisted post
    Post.objects.create(
        title=f"UNLISTED",
        description="A sample post.",
        content_type=Post.ContentType.PLAIN,
        content="This is a test post.",
        author=self.authors[0],
        visibility=Post.Visibility.UNLISTED
    )

    # Should not have the unlisted post
    response = self.client.get(reverse("posts", kwargs={ "author_id": self.authors[0].id }), { "size": 100 }).json()
    for post in response["items"]:
      self.assertNotEqual(post["visibility"], "FRIENDS")

    # Should now have the unlisted post
    self.client.session["id"] = self.authors[0].id
    response = self.client.get(reverse("posts", kwargs={ "author_id": self.authors[0].id }), { "size": 100 }).json()
    
    found_unlisted_visibility = next((True for post in response["items"] if post["visibility"] == "UNLISTED"), False)
    self.assertTrue(found_unlisted_visibility)

  def _is_post_object(self, obj):
    properties = ["type", "title", "id", "source", "origin", "description", "contentType", 
                  "content", "author", "count", "comments", "commentsSrc", "published", 
                  "visibility"]
    for property in properties:
      if not property in obj:
        return False
    return True

  def test_invalid_post_payload(self):
    pass

  def test_impersonation_post_payload(self):
    pass

  def test_valid_post_payload(self):
    pass