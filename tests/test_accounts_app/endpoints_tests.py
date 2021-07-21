from model_bakery import baker
from rest_framework import status
import pytest
import json

from accounts.models import Comment
from books.models import Book, Author


pytestmark = pytest.mark.django_db


class TestCommentEndpoints:

    endpoint = '/api/books/{book_id}/comments/'

    def test_retrieve(self, client, create_user):
        book = baker.make(Book)
        comment = baker.make(Comment, book=book, author=create_user)
        expected_json = {
            'id': comment.id,
            'author': str(comment.author),
            'book': str(comment.book),
            'created': comment.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'text': comment.text
        }
        url = self.endpoint.format(book_id=book.id) + f'{comment.id}/'

        response = client.get(url, follow=True, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert json.loads(response.content) == expected_json
    
    def test_list(self, client):
        book = baker.make(Book)
        baker.make(Comment, book=book, _quantity=3)

        response = client.get(self.endpoint.format(book_id=book.id), follow=True)

        assert response.status_code == status.HTTP_200_OK
        assert len(json.loads(response.content)) == 3

    def test_create(self, authenticated_client):
        client, user = authenticated_client
        book = baker.make(Book)
        payload = {
            'text': 'Здесь написан комментарий'
            # 'genre': 'horror',
        }
        expected_json = {
            'author': str(user),
            'text': 'Здесь написан комментарий'
            # 'genre': payload['genre'],
        }

        response = client.post(self.endpoint.format(book_id=book.id), payload, follow=True, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        expected_json['id'] = response.data['id']
        expected_json['created'] = response.data['created']
        assert response.data == expected_json

    def test_update(self, authenticated_client):
        client, user = authenticated_client
        book = baker.make(Book)
        comment = baker.make(Comment, author=user, book=book)
        payload = {
            'text': 'Здесь написан новый комментарий'
        }
        url = self.endpoint.format(book_id=book.id) + f'{comment.id}/'

        response = client.put(url, payload, follow=True, format='json')

        assert response.status_code == status.HTTP_200_OK
        expected_json = payload
        expected_json['id'] = response.data['id']
        expected_json['created'] = response.data['created']
        expected_json['author'] = str(user)
        assert json.loads(response.content) == expected_json

    @pytest.mark.parametrize('field_name', ['text'])
    def test_partial_update(self, authenticated_client, field_name):
        client, user = authenticated_client
        book = baker.make(Book, author=user)
        comment = baker.make(Comment, author=user, book=book)
        new_data = {
            'text': 'Здесь написан новый комментарий'
        }
        url = self.endpoint.format(book_id=book.id) + f'{comment.id}/'

        response = client.patch(url, {field_name: new_data[field_name]}, follow=True, format='json')
        expected_data = new_data[field_name]

        assert response.status_code == status.HTTP_200_OK
        assert json.loads(response.content)[field_name] == expected_data

    def test_destroy(self, authenticated_client):
        client, user = authenticated_client
        book = baker.make(Book, author=user)
        comment = baker.make(Comment, author=user, book=book)
        url = self.endpoint.format(book_id=book.id) + f'{comment.id}/'

        response = client.delete(url, follow=True, format='json')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Comment.objects.all().count() == 0


class TestAuthorEndpoints:

    endpoint = '/api/authors/'
    
    def test_list(self, client):
        baker.make(Author, _quantity=3)

        response = client.get(self.endpoint, follow=True)

        assert response.status_code == status.HTTP_200_OK
        assert len(json.loads(response.content)) == 3
