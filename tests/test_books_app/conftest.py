from rest_framework.test import APIClient
import pytest
# from pytest_django import fixtures

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def authenticated_client(django_user_model):
    username = 'user1'
    password = '123qwerty123'
    user = django_user_model.objects.create_user(username=username, password=password)
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user