from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=250)


class Book(models.Model):
    title = models.CharField(max_length=250)
    publ_year = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(3000)])
    author = models.ForeignKey(
        'Author',
        on_delete=models.CASCADE,
        related_name='books'
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.SET_NULL,
        related_name='books',
        blank=True,
        null=True
    )


class Library(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    # поля для времени работы
    opening_hours_from = models.TimeField()
    opening_hours_to = models.TimeField()


class Author(models.Model):
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    patronymic = models.CharField(max_length=250)
    birth_year = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(3000)])