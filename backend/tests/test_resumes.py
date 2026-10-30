import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from reportlab.pdfgen import canvas

from apps.resumes import matcher

RESUME = "Python developer with Django, REST API, PostgreSQL and Git experience. Built web apps."
JD = "We need a Python developer skilled in Django, PostgreSQL, Docker and AWS to build REST API services."


def make_pdf(text):
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    c.drawString(72, 750, text)
    c.save()
    return buf.getvalue()


def test_matcher_finds_missing_keywords():
    res = matcher.analyze(RESUME, JD)
    assert 0 < res["score"] <= 100
    assert "docker" in res["missing_keywords"]
    assert "django" in res["matched_keywords"]


def test_better_resume_scores_higher():
    better = RESUME + " Also Docker and AWS deployment."
    assert matcher.analyze(better, JD)["score"] > matcher.analyze(RESUME, JD)["score"]


def test_matcher_rejects_empty():
    with pytest.raises(ValueError):
        matcher.analyze("", JD)


def test_analyze_with_text(client):
    r = client.post("/api/resumes/analyze/", {"resume_text": RESUME, "job_description": JD}, format="json")
    assert r.status_code == 201
    assert "docker" in r.data["missing_keywords"]
    assert client.get("/api/resumes/").data["count"] == 1


def test_analyze_with_pdf(client):
    pdf = SimpleUploadedFile("cv.pdf", make_pdf(RESUME), content_type="application/pdf")
    r = client.post("/api/resumes/analyze/", {"file": pdf, "job_description": JD}, format="multipart")
    assert r.status_code == 201 and r.data["score"] > 0


def test_analyze_rejects_non_pdf(client):
    f = SimpleUploadedFile("cv.txt", b"hello", content_type="text/plain")
    r = client.post("/api/resumes/analyze/", {"file": f, "job_description": JD}, format="multipart")
    assert r.status_code == 400


def test_analyze_requires_resume(client):
    r = client.post("/api/resumes/analyze/", {"job_description": JD}, format="json")
    assert r.status_code == 400


def test_keywords_have_no_trailing_punctuation_or_filler_words():
    jd = "Associate Developer with Python or Java, SQL and Git basics. Good learning attitude and communication skills."
    res = matcher.analyze("Python developer with SQL and Git.", jd)
    words = res["missing_keywords"] + res["matched_keywords"]
    assert all(not w.endswith(".") for w in words)
    assert not {"good", "skills", "basics"} & set(words)
    assert "java" in res["missing_keywords"]
