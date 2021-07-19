from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    """
    Модель комментария пользователя
    """
    owner = models.ForeignKey(
        'User',
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
