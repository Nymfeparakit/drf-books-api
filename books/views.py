from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


from .models import Book, Genre, Author
from .serializers import BookSerializer, GenreSerializer, AuthorSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с книгами
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthor]


class GenreListView(generics.ListAPIView):
    """models.Model
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
