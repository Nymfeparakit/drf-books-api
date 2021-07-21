from rest_framework import serializers

from .models import Book, Genre, Author


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    genre = serializers.StringRelatedField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'publ_year', 'author', 'genre']
        read_only_fields = ('author',)

    def to_internal_value(self, data):
        if self.partial and not 'genre' in data:
            return super().to_internal_value(data)
        if not 'genre' in data:
            raise serializers.ValidationError("genre is a required field")
        genre_name = data.pop('genre')
        # валидируем все поля, кроме жанра
        validated_data = super().to_internal_value(data)
        return dict(validated_data, **{'genre': genre_name})

    def create(self, validated_data):
        genre_name = validated_data.pop('genre')
        if not Genre.objects.filter(name=genre_name).exists():
            raise serializers.ValidationError("Указанный жанр отсутствует")
        genre = Genre.objects.get(name=genre_name)
        return Book.objects.create(genre=genre, **validated_data)

    def update(self, instance, validated_data):
        if self.partial and not 'genre' in validated_data:
            return super().update(instance, validated_data)
        genre_name = validated_data.pop('genre')
        if not Genre.objects.filter(name=genre_name).exists():
            raise serializers.ValidationError("Указанный жанр отсутствует")
        instance = super().update(instance, validated_data)
        instance.genre = Genre.objects.get(name=genre_name)
        instance.save()
        return instance



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'birth_year']
