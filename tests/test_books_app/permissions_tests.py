import pytest
from rest_framework import status
from model_bakery import baker
import json

from books.models import Book


pytestmark = pytest.mark.django_db

class TestBookPermissions:

    endpoint = '/api/books/'

    def test_not_authenticated_can_not_create(self, client):
        payload = {
            'title': 'Вам и не снилось',
            'publ_year': 1984,
            'genre': 'horror',
        }

        response = client.post(self.endpoint, payload, follow=True, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_authenticated_can_list(self, client):
        baker.make(Book, _quantity=3)

        response = client.get(self.endpoint, follow=True, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert len(json.loads(response.content)) == 3

    def test_not_authenticated_can_not_update(self, client):
        book = baker.make(Book)
        payload = {
            'title': 'Вам и не снилось',
            'publ_year': 1984,
            'genre': 'horror',
        }
        url = f'{self.endpoint}{book.id}/'

        response = client.put(url, payload, follow=True, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_author_can_not_update(self, authenticated_client, create_user):
        client, user = authenticated_client
        book = baker.make(Book, author=create_user)
        payload = {
            'title': 'Вам и не снилось',
            'publ_year': 1984,
            'genre': 'horror',
        }
        url = f'{self.endpoint}{book.id}/'

        response = client.put(url, payload, follow=True, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_not_author_can_not_delete(self, authenticated_client, create_user):
        client, user = authenticated_client
        book = baker.make(Book, author=create_user)
        url = f'{self.endpoint}{book.id}/'

        response = client.delete(url, follow=True, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN
