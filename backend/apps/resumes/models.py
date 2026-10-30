from django.conf import settings
from django.db import models


class ResumeAnalysis(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="analyses"
    )
    application = models.ForeignKey(
        "applications.Application", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="analyses",
    )
    resume_text = models.TextField()
    job_description = models.TextField()
    score = models.PositiveSmallIntegerField()
    matched_keywords = models.JSONField(default=list)
    missing_keywords = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "resume analyses"
