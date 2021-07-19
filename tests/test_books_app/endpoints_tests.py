from books.models import Book, Genre
from rest_framework.test import APIClient
from model_bakery import baker
from rest_framework import status
import pytest


pytestmark = pytest.mark.django_db


class TestGenreEndpoints:

    endpoint = '/api/genres/'

    def test_retrieve(self, client):
        genre = baker.make(Genre)
        expected_json = {
            'id': genre.id,
            'name': genre.name
        }
        url = f'{self.endpoint}{genre.id}'

        response = client.get(url, follow=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_json
    
    def test_list(self, client):
        baker.make(Genre, _quantity=3)

        response = client.get(self.endpoint, follow=True)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3


class TestBookEndpoints:

    endpoint = '/api/books/'

    def test_retrieve(self, client):
        genre = baker.make(Genre)
        book = baker.make(Book, genre=genre)
        expected_json = {
            'id': book.id,
            'title': book.title,
            'publ_year': book.publ_year,
            'author': str(book.author),
            'genre': str(book.genre)
        }
        url = f'{self.endpoint}{book.id}'

        response = client.get(url, follow=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_json
    
    def test_list(self, client):
        baker.make(Book, _quantity=3)

        response = client.get(self.endpoint, follow=True)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create(self, authenticated_client):
        client, user = authenticated_client
        genre = baker.make(Genre, name='horror')
        payload = {
            'title': 'Вам и не снилось',
            'publ_year': 1984,
            'genre': 'horror',
        }
        expected_json = {
            'title': payload['title'],
            'publ_year': payload['publ_year'],
            'author': str(user),
            'genre': payload['genre'],
        }

        response = client.post(self.endpoint, payload, follow=True)

        assert response.status_code == status.HTTP_201_CREATED
        expected_json['id'] = response.data['id']
        assert response.data == expected_json