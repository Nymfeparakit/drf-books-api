from django.db import models
from django.conf import settings


class Comment(models.Model):
    """
    Модель комментария пользователя
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='comments',
        null=True
    )
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
