from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from ..models import Group, Post


class StaticURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Тестовые данные"""
        cls.user = get_user_model().objects.create_user(username="Leon")

        cls.list_pages = {
            reverse("index"): "index.html",
            reverse("group_post", args=["test-lev"]): "group.html",
            # reverse("new_post"): "add_or_change_post.html",
            reverse("profile", args=[cls.user]): "profile.html",
            reverse("post", args=[cls.user, 1]): "post.html",
            # reverse("post_edit", args=[cls.user, 1]): "add_or_change_post.html",
            reverse("about:author"): "about/author.html",
            reverse("about:tech"): "about/tech.html"

        }

        cls.group = Group.objects.create(
            title="Заголовок группы",
            slug="test-lev",
            description="Тестовый текст группы"
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый текст поста"
        )

    def setUp(self) -> None:
        """Тестовые пользователи"""
        self.guest_client = Client()
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)

    def test_all_pages_urls(self):
        """Проверка страниц на статус 200"""
        for page, templates in self.list_pages.items():
            response = self.guest_client.get(page)
            self.assertEqual(response.status_code, 200,
                             f"Страница {page} не работает")

    def test_all_templates(self):
        """Проверка шаблонов"""
        for page, templates in self.list_pages.items():
            response = self.guest_client.get(page)
            self.assertTemplateUsed(response, templates,
                                    f"Шаблон {templates} не работае")

    def test_new_post_200(self):
        """Проверка статус код 200 new_post"""
        response = self.authorized_user.get(reverse("new_post"))
        self.assertEqual(response.status_code, 200)

    def test_post_edit_200(self):
        """Проверка статус код 200 post_edit"""
        response = self.authorized_user.get(
            reverse("post_edit", args=[self.user, 1]))
        self.assertEqual(response.status_code, 200)

    def test_not_authorized_user_new_post_redirect(self):
        """Проверка статус код 302 редирект new_post"""
        response = self.guest_client.get(reverse("new_post"))
        self.assertEqual(response.status_code, 302)

    def test_not_authorized_user_post_edit_redirect(self):
        """Проверка статус код 302 редирект post_edit"""
        response = self.guest_client.get(reverse("post_edit", args=[self.user, 1]))
        self.assertEqual(response.status_code, 302)

    def test_page404(self):
        """Проверка пустой страницы. Статус код 404"""
        response = self.guest_client.get("404/")
        self.assertEqual(response.status_code, 404, "Статус код 200???")

    # def test_new_redirect(self):
    #     form_data = {
    #         "text": "test-text",
    #         "group": self.group.id
    #     }
    #     response = self.authorized_user.post(
    #         reverse("post_edit", args=[self.user, 1, "edit/"]),
    #         data=form_data,
    #         follow=True)
    #     self.assertRedirects(response, "Alex/1/edit/")

    # def test_index_url(self):
    #     """Тест index.html код 200"""
    #     # "about/author/": "about/author.html"
    #     response = self.guest_client.get("about/author/")
    #     self.assertEqual(response.status_code, 200, "Не возврощает код 200")

    # def test_index_page_template(self):
    #     """Тест index.html шаблон"""
    #     response = self.guest_client.get(
    #         reverse("group_post", kwargs={"slug": "test-lev"}))
    #     self.assertEqual(response.status_code, 200, "Не возврощает код 200")
    #     self.assertTemplateUsed(response, "group.html", "Шаблон не работает")
