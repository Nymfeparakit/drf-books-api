from books.models import Book, Genre
from model_bakery import baker
from rest_framework import status
import pytest
import json


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


@pytest.fixture
def horror_genre(db):
    return baker.make(Genre, name='horror')


@pytest.mark.usefixtures('horror_genre')
class TestBookEndpoints:

    endpoint = '/api/books/'


    def test_retrieve(self, client, horror_genre):
        book = baker.make(Book, genre=horror_genre)
        expected_json = {
            'id': book.id,
            'title': book.title,
            'publ_year': book.publ_year,
            'author': str(book.author),
            'genre': 'horror'
        }
        url = f'{self.endpoint}{book.id}/'

        response = client.get(url, follow=True, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert json.loads(response.content) == expected_json
    
    def test_list(self, client):
        baker.make(Book, _quantity=3)

        response = client.get(self.endpoint, follow=True)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create(self, authenticated_client, horror_genre):
        client, user = authenticated_client
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

        response = client.post(self.endpoint, payload, follow=True, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        expected_json['id'] = response.data['id']
        assert response.data == expected_json

    def test_update(self, authenticated_client, horror_genre):
        client, user = authenticated_client
        book = baker.make(Book, author=user, genre=horror_genre)
        payload = {
            'title': 'new title',
            'publ_year': 1984,
            'genre': 'horror',
        }
        url = f'{self.endpoint}{book.id}/'

        response = client.put(url, payload, follow=True, format='json')

        assert response.status_code == status.HTTP_200_OK
        expected_json = payload
        expected_json['id'] = response.data['id']
        expected_json['author'] = response.data['author']
        assert json.loads(response.content) == expected_json

    @pytest.mark.parametrize('field_name', ['title', 'publ_year'])
    def test_partial_update(self, authenticated_client, field_name):
        client, user = authenticated_client
        book = baker.make(Book, author=user)
        new_data = {
            'title': 'new title',
            'publ_year': 1984
        }
        url = f'{self.endpoint}{book.id}/'

        response = client.patch(url, {field_name: new_data[field_name]}, follow=True, format='json')
        expected_data = new_data[field_name]

        assert response.status_code == status.HTTP_200_OK
        assert json.loads(response.content)[field_name] == expected_data

    def test_destroy(self, authenticated_client):
        client, user = authenticated_client
        book = baker.make(Book, author=user)
        url = f'{self.endpoint}{book.id}/'

        response = client.delete(url, follow=True, format='json')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Book.objects.all().count() == 0

