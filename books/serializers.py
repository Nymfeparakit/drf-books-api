from rest_framework import serializers

from .models import Book, Genre


class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    genre = serializers.StringRelatedField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'publ_year', 'author', 'genre']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']