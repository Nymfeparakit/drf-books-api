from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics

from .models import Book, Genre, Author
from .serializers import BookSerializer, GenreSerializer, AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с книгами
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class GenreListView(generics.ListAPIView):
    """
    View для получения списка жанров 
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreRetrieveView(generics.RetrieveAPIView):
    """
    View для получения конкретного жанра 
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class AuthorListView(generics.ListAPIView):
    """
    View для получения списка авторов
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
