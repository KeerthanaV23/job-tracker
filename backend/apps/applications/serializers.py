from rest_framework import serializers

from .models import Application, StatusHistory


class StatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusHistory
        fields = ("id", "from_status", "to_status", "changed_at")


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "id", "company", "role", "location", "job_url", "job_description",
            "salary", "notes", "status", "applied_date", "interview_at",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
