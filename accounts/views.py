from django.shortcuts import render
from rest_framework import viewsets

from .models import Comment
from .serializers import CommentSerializer
from books.views import IsAuthor


class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset для комментариев пользователей
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor,]
