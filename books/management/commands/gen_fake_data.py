from django.core.management.base import BaseCommand
import csv
from django.contrib.auth.models import User
from mimesis import Person, Datetime, Address
from mimesis.builtins import RussiaSpecProvider
import random
from django.contrib.auth.hashers import make_password
from uuid import uuid4

from books.models import Genre, Book, Author
from accounts.models import Comment


genres_names = ['Detective', 'Fantasy', 'Fiction', 'Thriller', 'Horror', 'Sci-Fi', 'Romace', 'Short stories']
COMMENTS_TEXT = ['Здесь есть комментарий', 'Ну такое', 'Очень даже ничего', 'Не читал, но осуждаю', 'Превосходно']
# Максимальное количество одновременно вставляемых строк, чтобы не превысить максимальное число вставляемых в sqlite элементов
MAX_BATCH_SIZE = 500 
AUTHORS_NUM = 500
BOOKS_PER_AUTHOR_NUM = 5
COMMENTS_PER_BOOK_NUM = 5


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными"

    def fill_genres(self):
        # генерируем жанры
        genres_objs = [Genre(name=name) for name in genres_names]
        Genre.objects.bulk_create(genres_objs)
        self.stdout.write("Заполнены жанры")

    def fill_authors(self, fake_date, fake_person):
        ru_provider = RussiaSpecProvider()
        # генерируем авторов
        author_objs = []
        for i in range(AUTHORS_NUM):
            author = Author(
                username=str(uuid4()),
                password=make_password('123qwerty123'),
                email=fake_person.email(unique=True),
                first_name=fake_person.name(),
                last_name=fake_person.surname(),
                patronymic=ru_provider.patronymic(),
                birth_year=fake_date.year()
            )
            author_objs.append(author)
        Author.objects.bulk_create(author_objs)
        self.stdout.write("Заполнены авторы")

    def fill_books(self, fake_date, fake_person):
        fake_address = Address()
        genres_objs = list(Genre.objects.all())
        books_objs = []
        for i, author in enumerate(Author.objects.all()):
            # Добавляем для каждого автора книги
            for j in range(BOOKS_PER_AUTHOR_NUM):
                books_objs.append(Book(
                    genre=random.choice(genres_objs),
                    author=author,
                    publ_year=fake_date.year(),
                    title=f'{fake_person.name()} in {fake_address.city()}'
                ))
                if (i+1)*(j+1) % MAX_BATCH_SIZE:
                    Book.objects.bulk_create(books_objs)
                    books_objs = []
        self.stdout.write("Заполнены книги")

    def fill_comments(self):
        comments_objs = []
        authors_list = list(Author.objects.all())
        for i, book in enumerate(Book.objects.all()):
            # Добавляем для каждой книги комментарии
            for j in range(COMMENTS_PER_BOOK_NUM):
                comments_objs.append(Comment(
                    author=random.choice(authors_list),
                    book=book,
                    text=random.choice(COMMENTS_TEXT)
                ))
                if (i+1)*(j+1) % MAX_BATCH_SIZE:
                    Comment.objects.bulk_create(comments_objs)
                    comments_objs = []
        self.stdout.write("Заполнены комментарии")

    def handle(self, *args, **options):
        fake_person = Person('ru')
        fake_date = Datetime()

        self.fill_genres()
        self.fill_authors(fake_date, fake_person)
        self.fill_books(fake_date, fake_person)
        self.fill_comments()

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно сгенерированы"))
