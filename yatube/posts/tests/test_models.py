from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Group, Post


class ModelFieldsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Тестовые данные"""
        cls.user = get_user_model().objects.create_user(username="Leon")

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

    def test_post_model_fields(self):
        """Тест значений полей Verbose_name модели Post"""
        field_verbose = {
            "author": "Автор поста",
            "text": "Текст",
            "group": "Название сообщества"
        }
        for field, value in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(self.post._meta.get_field(field).verbose_name,
                                 value)

    def test_group_model_fields(self):
        """Тест значений полей Verbose_name модели Group"""
        field_verbose = {
            "title": "Заголовок сообщества",
            "slug": "Адрес сообщества в интернете",
            "description": "Описание сообщества"
        }
        for field, value in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(self.group._meta.get_field(field).verbose_name,
                                 value)

    def test_help_text_post(self):
        """Тест значений полей help_text модели Post"""
        field_help_text = {
            "author": "User создавший пост",
            "text": "Цитата, статья, текст.",
            "group": "Названия сообщества по интересам."
        }
        for field, value in field_help_text.items():
            with self.subTest(value=value):
                self.assertEqual(self.post._meta.get_field(field).help_text,
                                 value)

    def test_post_str(self):
        """Тест Post __str метод"""
        value = self.post.__str__()
        expected = self.post.text[:15]
        self.assertEqual(value, expected, "__str__() не работает.")

    def test_group_str(self):
        """Тест Group __str метод"""
        value = self.group.__str__()
        expected = self.group.title
        self.assertEqual(value, expected, "__str__() не работает.")
