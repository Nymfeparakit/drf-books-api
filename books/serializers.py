from rest_framework import serializers

from .models import Book, Genre, Author


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    genre = GenreSerializer()
    class Meta:
        model = Book
        fields = ['id', 'title', 'publ_year', 'author', 'genre']
        read_only_fields = ('author',)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'birth_year']
