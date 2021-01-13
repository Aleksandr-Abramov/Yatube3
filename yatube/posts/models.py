from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    """Модель создания поста"""
    text = models.TextField(
        verbose_name="Текст",
        help_text="Цитата, статья, текст."
    )
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(
        User,
        verbose_name="Автор поста",
        on_delete=models.CASCADE,
        related_name="posts",
        help_text="User создавший пост"
    )

    group = models.ForeignKey(
        "Group",
        verbose_name="Название сообщества",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="group",
        help_text="Названия сообщества по интересам."
    )

    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    """Модель для Группы"""
    title = models.CharField(verbose_name="Заголовок сообщества", max_length=255)
    slug = models.SlugField(verbose_name="Адрес сообщества в интернете", unique=True)
    description = models.TextField(verbose_name="Описание сообщества")

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель для Комментариев"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
