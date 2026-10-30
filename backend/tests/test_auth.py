import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_login_me():
    c = APIClient()
    r = c.post("/api/auth/register/", {"email": "new@example.com", "password": "Str0ngPass!23"})
    assert r.status_code == 201
    assert "password" not in r.data

    r = c.post("/api/auth/login/", {"email": "new@example.com", "password": "Str0ngPass!23"})
    assert r.status_code == 200 and "access" in r.data

    c.credentials(HTTP_AUTHORIZATION=f"Bearer {r.data['access']}")
    me = c.get("/api/auth/me/")
    assert me.status_code == 200 and me.data["email"] == "new@example.com"


@pytest.mark.django_db
def test_weak_password_rejected():
    r = APIClient().post("/api/auth/register/", {"email": "x@example.com", "password": "12345678"})
    assert r.status_code == 400


@pytest.mark.django_db
def test_protected_requires_token():
    assert APIClient().get("/api/applications/").status_code == 401
