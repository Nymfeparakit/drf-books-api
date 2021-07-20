from rest_framework import serializers

from .models import Comment
from books.models import Book


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    book = serializers.StringRelatedField()
    class Meta:
        model = Comment
        fields = ['id', 'author', 'book', 'created', 'text']
        read_only_fields = ('created',)

    def create(self, validated_data):
        book = Book.objects.get(pk=self.context["view"].kwargs["book_pk"])
        validated_data["book"] = book
        return Comment.objects.create(**validated_data)
