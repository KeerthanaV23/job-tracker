from django.conf import settings
from rest_framework import serializers

from apps.applications.models import Application

from .models import ResumeAnalysis


class AnalyzeRequestSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    resume_text = serializers.CharField(required=False, allow_blank=True)
    job_description = serializers.CharField()
    application = serializers.PrimaryKeyRelatedField(
        queryset=Application.objects.all(), required=False, allow_null=True
    )

    def validate_file(self, f):
        if not f.name.lower().endswith(".pdf"):
            raise serializers.ValidationError("Only PDF files are supported.")
        if f.size > settings.MAX_RESUME_UPLOAD_MB * 1024 * 1024:
            raise serializers.ValidationError(f"Max file size is {settings.MAX_RESUME_UPLOAD_MB} MB.")
        return f

    def validate_application(self, app):
        if app and app.user_id != self.context["request"].user.id:
            raise serializers.ValidationError("Invalid application.")
        return app

    def validate(self, attrs):
        if not attrs.get("file") and not attrs.get("resume_text", "").strip():
            raise serializers.ValidationError("Upload a PDF resume or paste resume_text.")
        return attrs


class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = ("id", "application", "score", "matched_keywords", "missing_keywords", "created_at")
