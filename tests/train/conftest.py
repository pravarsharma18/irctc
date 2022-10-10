from rest_framework.test import APIClient
from base.choices import UserRole
from django.contrib.auth import get_user_model
import pytest

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(role=UserRole.STUDENT.name, is_admin=False):
        return api_client.force_authenticate(user=User(role=role, is_admin=is_admin))
    return do_authenticate


@pytest.fixture
def create_book(api_client):
    def do_create_book(book):
        return api_client.post("/books/", data=book)
    return do_create_book


@pytest.fixture
def create_category(api_client):
    def do_create_category(category):
        return api_client.post('/books/category/', category)
    return do_create_category
