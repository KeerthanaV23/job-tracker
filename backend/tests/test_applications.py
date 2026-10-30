from datetime import timedelta

import pytest
from django.core import mail
from django.utils import timezone
from rest_framework.test import APIClient

from apps.applications.models import Application
from apps.applications.tasks import send_interview_reminders


def make(client, **kw):
    payload = {"company": "Acme", "role": "Python Developer", "status": "applied"}
    payload.update(kw)
    return client.post("/api/applications/", payload, format="json")


def test_create_and_list(client):
    r = make(client)
    assert r.status_code == 201
    assert client.get("/api/applications/").data["count"] == 1


def test_users_only_see_own_data(client, other_user):
    make(client)
    c2 = APIClient()
    c2.force_authenticate(other_user)
    assert c2.get("/api/applications/").data["count"] == 0


def test_filter_and_search(client):
    make(client, company="Zoho", role="Backend", status="interview")
    make(client, company="TCS", role="Django Dev", status="applied")
    assert client.get("/api/applications/?status=interview").data["count"] == 1
    assert client.get("/api/applications/?search=tcs").data["count"] == 1


def test_status_change_creates_history(client):
    app_id = make(client).data["id"]
    client.patch(f"/api/applications/{app_id}/", {"status": "interview"}, format="json")
    client.patch(f"/api/applications/{app_id}/", {"status": "offer"}, format="json")
    hist = client.get(f"/api/applications/{app_id}/history/").data
    assert [h["to_status"] for h in hist] == ["applied", "interview", "offer"]


def test_interview_reminder_task(client, user):
    soon = timezone.now() + timedelta(hours=5)
    later = timezone.now() + timedelta(days=5)
    Application.objects.create(user=user, company="A", role="r", status="interview", interview_at=soon)
    Application.objects.create(user=user, company="B", role="r", status="interview", interview_at=later)
    assert send_interview_reminders() == 1
    assert len(mail.outbox) == 1
    assert send_interview_reminders() == 0  # not sent twice
