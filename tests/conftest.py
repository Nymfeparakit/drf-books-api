from rest_framework.test import APIClient
import pytest
from mimesis import Person 
# from pytest_django import fixtures

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def create_user(django_user_model):
    fake_person = Person('en')
    username = fake_person.username()
    password = '123qwerty123'
    return django_user_model.objects.create_user(username=username, password=password)

@pytest.fixture
def authenticated_client(django_user_model):
    fake_person = Person('en')
    username = fake_person.username()
    password = '123qwerty123'
    user = django_user_model.objects.create_user(username=username, password=password)
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user