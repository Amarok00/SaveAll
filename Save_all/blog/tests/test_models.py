# -*- coding: utf-8 -*-
from blog.models import Post
import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

#  этот test_title_create - must not pass
# @pytest.mark.django_db
# def test_title_create():
#     article = Post.objects.create(title="article1")
#     assert article.title == "article1"

class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for the author of the post
        cls.author = User.objects.create_user(username='testuser', password='testpassword')

        # Create a Post object for testing
        cls.post = Post.objects.create(
            title='Test Post',
            content='This is a test post',
            author=cls.author,
            slug='test-post',
        )
        
        cls.post.likes_post.add(cls.author)
        cls.post.saves_posts.add(cls.author)

    def test_title_max_length(self):
        max_length = self.post._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_content_max_length(self):
        max_length = self.post._meta.get_field('content').max_length
        self.assertEqual(max_length, 5000)

    def test_data_create_default(self):
        self.assertEqual(self.post.data_create.date(), timezone.now().date())

    def test_data_update_auto_now(self):
        old_data_update = self.post.data_update
        self.post.title = 'Updated Test Post'
        self.post.save()
        self.assertNotEqual(self.post.data_update, old_data_update)

    def test_author_foreign_key(self):
        self.assertEqual(self.post.author, self.author)

    def test_slug_max_length(self):
        max_length = self.post._meta.get_field('slug').max_length
        self.assertEqual(max_length, 50)

    def test_likes_post_many_to_many(self):
        self.post.likes_post.add(self.author)
        self.assertTrue(self.author in self.post.likes_post.all())

    def test_saves_posts_many_to_many(self):
        self.post.saves_posts.add(self.author)
        self.assertTrue(self.author in self.post.saves_posts.all())

    def test_total_likes_post(self):
        self.assertEqual(self.post.total_likes_post(), 1)

    def test_total_saves_posts(self):
        self.assertEqual(self.post.total_saves_posts(), 1)

    # def test_get_absolute_url(self):
    #     expected_url = f'/posts/{self.post.pk}/'
    #     self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_str_representation(self):
        self.assertEqual(str(self.post), 'Test Post')