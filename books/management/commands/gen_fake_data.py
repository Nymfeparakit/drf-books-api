from django.core.management.base import BaseCommand
import csv
from django.contrib.auth.models import User
from mimesis import Person, Datetime
from mimesis.builtins import RussiaSpecProvider
import random

from .models import Genre


genres = ['Detective', 'Fantasy', 'Fiction', 'Thriller', 'Horror', 'Sci-Fi', 'Romace', 'Short stories']

class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными"

    def handle(self, *args, **options):
        ru_provider = RussiaSpecProvider()
        # генерируем жанры
        genres_objs = []
        for name in genres_names:
            genre = Genre(name=name)
        genres_list = list(Genre.objects.bulk_create(genres_objs))
        fake = Faker()
        users_objs = []
        fake_person = Person(locale=locale.RU)
        fake_date = Datetime()
        # генерируем пользователей
        for i in range(500):
            users_objs.append(User(
                username=person.name(),
                first_name=person.first_name(),
                last_name=person.last_name(),
                password='123qwerty123'
            ))
        User.objects.bulk_create(users_objs)
        # сопоставляем с ними авторов
        authors_objs = []
        for i, user in enumerate(User.objects.all()):
            author = Author(
                user=user,
                patronymic=ru_provider.patronymic(),
                birth_year=fake_date.year()
            )
            authors_objs.append(author)
            # Добавляем для автора 5 книг
            books_objs = []
            for j in range(5):
                books_objs.append(Book(
                    genre=random.choice(genres_list),
                    author=author,
                    publ_year=fake_date.year(),
                    title = fake_person.name()
                ))
            Book.objects.create_bulk(books_objs)

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно сгенерированы"))
