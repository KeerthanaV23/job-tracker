import pytest
from rest_framework.test import APIClient

from apps.users.models import User


def make(client, status):
    return client.post("/api/applications/", {"company": "C", "role": "R", "status": status}, format="json").data["id"]


def test_summary_and_funnel(client):
    a = make(client, "applied")
    make(client, "applied")
    client.patch(f"/api/applications/{a}/", {"status": "interview"}, format="json")
    data = client.get("/api/analytics/summary/").data
    assert data["total"] == 2
    assert data["by_status"]["interview"] == 1
    assert data["funnel"]["interview"] == 1
    assert data["funnel"]["interview_rate"] == 50.0


def test_admin_stats_permission(client, db):
    assert client.get("/api/analytics/admin-stats/").status_code == 403
    admin = User.objects.create_user(email="admin@example.com", password="Str0ngPass!23", role="admin")
    c = APIClient()
    c.force_authenticate(admin)
    r = c.get("/api/analytics/admin-stats/")
    assert r.status_code == 200 and r.data["users"] >= 1
