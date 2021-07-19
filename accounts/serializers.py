from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    book = serializers.StringRelatedField()
    class Meta:
        model = Comment
        fields = ['id', 'owner', 'book', 'created', 'text']
