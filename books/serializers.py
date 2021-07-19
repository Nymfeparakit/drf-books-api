from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    genre = serializers.StringRelatedField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'publ_year', 'author', 'genre']
