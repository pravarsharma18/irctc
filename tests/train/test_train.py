import pytest
from rest_framework import status
from model_bakery import baker

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


@pytest.mark.django_db
class TestTrain:
    def test_if_test_data_is_not_given_return_400(self, api_client):
        pass
