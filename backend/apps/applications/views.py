from drf_spectacular.utils import extend_schema
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Application, StatusHistory
from .serializers import ApplicationSerializer, StatusHistorySerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    """CRUD for the logged-in user's applications. Supports ?status=, ?search=, ?ordering=."""

    serializer_class = ApplicationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["company", "role", "location", "notes"]
    ordering_fields = ["applied_date", "updated_at", "company"]

    def get_queryset(self):
        qs = Application.objects.filter(user=self.request.user)
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs

    def perform_create(self, serializer):
        app = serializer.save(user=self.request.user)
        StatusHistory.objects.create(application=app, from_status="", to_status=app.status)

    def perform_update(self, serializer):
        old_status = serializer.instance.status
        old_interview = serializer.instance.interview_at
        app = serializer.save()
        if app.status != old_status:
            StatusHistory.objects.create(
                application=app, from_status=old_status, to_status=app.status
            )
        if app.interview_at != old_interview and app.reminder_sent:
            app.reminder_sent = False  # interview moved -> remind again
            app.save(update_fields=["reminder_sent"])

    @extend_schema(responses=StatusHistorySerializer(many=True))
    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        app = self.get_object()
        return Response(StatusHistorySerializer(app.history.all(), many=True).data)
