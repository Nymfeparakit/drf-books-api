import pytest
from rest_framework import status
from model_bakery import baker
import json

from accounts.models import Comment
from books.models import Book


pytestmark = pytest.mark.django_db

class TestCommentPermissions:

    endpoint = '/api/books/{book_id}/comments/'

    def test_not_authenticated_can_not_create(self, client):
        book = baker.make(Book)
        payload = {
            'text': 'Здесь написан комментарий'
        }

        response = client.post(self.endpoint.format(book_id=book.id), payload, follow=True, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_authenticated_can_list(self, client):
        book = baker.make(Book)
        baker.make(Comment, book=book, _quantity=3)

        response = client.get(self.endpoint.format(book_id=book.id), follow=True, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert len(json.loads(response.content)['results']) == 3

    def test_not_authenticated_can_not_update(self, client):
        book = baker.make(Book)
        comment = baker.make(Comment, book=book)
        payload = {
            'text': 'Здесь есть комментарий',
        }
        url = self.endpoint.format(book_id=book.id) + f'{comment.id}/'

        response = client.put(url, payload, follow=True, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_author_can_not_update(self, authenticated_client, create_user):
        client, user = authenticated_client
        book = baker.make(Book)
        comment = baker.make(Comment, book=book, author=create_user)
        payload = {
            'text': 'Здесь есть комментарий',
        }
        url = self.endpoint.format(book_id=book.id) + f'{comment.id}/'

        response = client.put(url, payload, follow=True, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_not_author_can_not_delete(self, authenticated_client, create_user):
        client, user = authenticated_client
        book = baker.make(Book)
        comment = baker.make(Comment, book=book, author=create_user)
        url = self.endpoint.format(book_id=book.id) + f'{comment.id}/'

        response = client.delete(url, follow=True, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN
