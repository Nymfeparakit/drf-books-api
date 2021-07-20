from django.core.management.base import BaseCommand
import csv
from django.contrib.auth.models import User
from mimesis import Person, Datetime
from mimesis.builtins import RussiaSpecProvider
import random
from django.contrib.auth.hashers import make_password

from books.models import Genre, Book, Author


genres_names = ['Detective', 'Fantasy', 'Fiction', 'Thriller', 'Horror', 'Sci-Fi', 'Romace', 'Short stories']
# Максимальное количество одновременно вставляемых строк, чтобы не превысить максимальное число вставляемых в sqlite элементов
MAX_BATCH_SIZE = 500 
AUTHORS_NUM = 500
BOOKS_PER_AUTHOR_NUM = 5

class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными"

    def fill_genres(self):
        # генерируем жанры
        genres_objs = [Genre(name=name) for name in genres_names]
        return Genre.objects.bulk_create(genres_objs)

    def handle(self, *args, **options):
        ru_provider = RussiaSpecProvider()
        fake_person = Person('en')
        fake_date = Datetime()

        # заполняем БД жанрами
        genres_list = list(self.fill_genres())

        # итерация, после которой будут вставляться книги
        iter_to_create = AUTHORS_NUM / (AUTHORS_NUM * BOOKS_PER_AUTHOR_NUM / MAX_BATCH_SIZE)

        # генерируем авторов
        author_objs = []
        for i in range(50):
            author = Author(
                username=fake_person.email(unique=True),
                password=make_password('123qwerty123'),
                first_name=fake_person.name(),
                last_name=fake_person.surname(),
                patronymic=ru_provider.patronymic(),
                birth_year=fake_date.year()
            )
            author_objs.append(author)
        Author.objects.bulk_create(author_objs)
        books_objs = []
        for author in Author.objects.all():
            # Добавляем для автора 5 книг
            books_objs = []
            for j in range(5):
                books_objs.append(Book(
                    genre=random.choice(genres_list),
                    author=author,
                    publ_year=fake_date.year(),
                    title = fake_person.name()
                ))
        Book.objects.bulk_create(books_objs)


        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно сгенерированы"))
