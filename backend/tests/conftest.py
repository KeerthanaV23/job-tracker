import pytest
from rest_framework.test import APIClient

from apps.users.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(email="a@example.com", password="Str0ngPass!23", first_name="Asha")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(email="b@example.com", password="Str0ngPass!23")


@pytest.fixture
def client(user):
    c = APIClient()
    c.force_authenticate(user)
    return c
