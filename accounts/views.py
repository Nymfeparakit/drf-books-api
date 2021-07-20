from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from .models import Comment
from .serializers import CommentSerializer
from books.views import IsAuthorOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset для комментариев пользователей
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly,]

    def get_queryset(self):
        return Comment.objects.filter(book=self.kwargs['book_pk'])
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)

