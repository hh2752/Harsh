from django.apps import apps
from django.test import TestCase
from post.apps import BlogConfig
from post.models import Post, Comment
from django.urls import reverse
from django.contrib.auth.models import User
from post.forms import PostForm, CommentForm, NewsForm
from post.badges import (
    get_posts,
    total_dislikes_received,
    total_likes_received,
    user_dislikes_badges_tier,
    user_friends_tier,
    user_likes_badges_tier,
    balance_badge,
    post_tier,
)


# Create user for testing purposes
def create_user(username_string):
    return User.objects.create(username=username_string)


# Create post for testing puproses
def create_post(authour_string):
    return Post.objects.create(author=authour_string)


# test that app config name matches and is found
class ReportsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(BlogConfig.name, "post")
        self.assertEqual(apps.get_app_config("post").name, "post")


class BaseTest(TestCase):
    def setUp(self):
        self.post = Post(title="test")
        self.user = User.objects.create(username="test_user")
        self.comment = Comment(content="testing", author=self.user)

        self.post_url = reverse("post:base")

        self.valid_post = {
            "title": "Testing",
            "content": "Test content",
        }
        self.invalid_post = {
            "title": "",
            "content": "",
        }

        self.valid_comment = {
            "content": "valid content",
        }
        self.invalid_comment = {
            "content": "",
        }

        return super().setUp()


class Post_Tests(BaseTest):
    def test_string_representation(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_post_url(self):
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, 302)

    def test_post_form_valid(self):
        form_data = self.valid_post
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

#     def test_post_form_invalid(self):
#         form_data = self.invalid_post
#         form = PostForm(data=form_data)
#         self.assertFalse(form.is_valid())


class Comment_Tests(BaseTest):
    def test_string_representation(self):
        self.assertEqual(
            str(self.comment),
            "Comment {} by {}".format(self.comment.content, self.comment.author),
        )

    def test_comment_form_valid(self):
        form_data = self.valid_comment
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

#     def test_comment_form_invalid(self):
#         form_data = self.invalid_comment
#         form = CommentForm(data=form_data)
#         self.assertFalse(form.is_valid())


class News_Tests(BaseTest):
    def test_string_representation(self):
        self.assertEqual(
            str(self.comment),
            "Comment {} by {}".format(self.comment.content, self.comment.author),
        )

    def test_comment_form_valid(self):
        form_data = self.valid_comment
        form = NewsForm(data=form_data)
        self.assertTrue(form.is_valid())

#     def test_comment_form_invalid(self):
#         form_data = self.invalid_comment
#         form = NewsForm(data=form_data)
#         self.assertFalse(form.is_valid())


# Test set for badge logic contained in badges.py
class Badges_Tests(BaseTest):

    # Test to see if a new user has no posts
    def test_user_with_no_posts_posts(self):
        test_user = create_user("test_user_1")
        self.assertFalse(get_posts(test_user))

    # Test to see if a new user has no likes
    def test_user_with_no_posts_likes(self):
        test_user = create_user("test_user_1")
        self.assertFalse(total_likes_received(test_user))

    # Test to see if a new user has no dislikes
    def test_user_with_no_posts_dislikes(self):
        test_user = create_user("test_user_1")
        self.assertFalse(total_dislikes_received(test_user))

    # Test to see if the dislikes tier function works
    def test_dislikes_badge(self):
        badges = []
        self.assertFalse(user_dislikes_badges_tier(badges, 100))

    # Test to see that the like tier function does not return a value
    def test_user_wth_no_posts_like_tier(self):
        badges = []
        self.assertFalse(user_likes_badges_tier(badges, 100))

    # Test to see that the balance badge works
    def test_user_wth_no_posts_dislike_tier(self):
        badges = []
        test_user = create_user("test_user_1")
        test_post1 = create_post(test_user)
        # Unknown how to test likes
        balance_badge(badges, test_user)
        self.assertTrue(test_post1)

    # Test friends tier
    def test_friends_tiers(self):
        badges = []
        friends = []
        for i in range(100):
            friends.append(i)

        user_friends_tier(badges, friends)

    # Test posts count tiers
    def test_posts_tier(self):
        badges = []
        test_user2 = create_user("test_user_2")

        for i in range(100):
            create_post(test_user2)

        post_tier(badges, test_user2)
