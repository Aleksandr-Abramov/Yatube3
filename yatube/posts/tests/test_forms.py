import os
import shutil
import tempfile
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from ..forms import PostForm
from ..models import Post, Group


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Тестовые данные"""
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.form = PostForm()
        cls.user = get_user_model().objects.create_user(username="Alex")
        cls.group = Group.objects.create(
            title="Заголовок группы",
            slug="test-lev",
            description="Тестовый текст группы"
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="тестовый текст поста",
            group=cls.group
        )

    def setUp(self) -> None:
        """Тестовые пользователи"""
        self.authorized_guest = Client()
        self.authorized_guest.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_create_post_and_redirect(self):
        """Тест код 200, редирект и сохранения данных"""
        small_gif = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
                     b'\x01\x00\x80\x00\x00\x00\x00\x00'
                     b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                     b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                     b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                     b'\x0A\x00\x3B'
                     )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            "text": "test-text",
            "group": self.group.id,
            "image": uploaded
        }


        tasks_count = Post.objects.count()
        response = self.authorized_guest.post(
            reverse("new_post"),
            data=form_data,
            follow=True)

        self.assertEqual(response.status_code, 200, "Страница new.html не отвечает")
        self.assertRedirects(response, "/")
        self.assertEqual(Post.objects.count(), tasks_count + 1,
                         f"Количество постов меньше {tasks_count + 1}")

    def test_change_post_and_redirect(self):
        """Тест код 200, редирект и изменение данных"""
        form_data = {
            "text": "test-text",
            "group": self.group.id
        }

        response = self.authorized_guest.post(
            reverse("post_edit", args=[self.user, 1]),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200,
                         "Страница add_or_change_post.html не отвечает")
        self.assertEqual(Post.objects.first().text, form_data["text"],
                         "Пост не миняется.")
        self.assertRedirects(
            response,
            reverse("post", args=[self.user, self.post.id]))
