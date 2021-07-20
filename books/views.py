from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT


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
    permission_classes = [IsAuthorOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)


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
