from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncWeek
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.applications.models import Application, StatusHistory
from apps.users.permissions import IsAdminRole


class SummaryView(APIView):
    """Dashboard numbers for the current user: status counts, weekly trend, funnel."""

    def get(self, request):
        apps = Application.objects.filter(user=request.user)
        by_status = {s: 0 for s, _ in Application.Status.choices}
        for row in apps.values("status").annotate(n=Count("id")):
            by_status[row["status"]] = row["n"]

        since = timezone.localdate() - timedelta(weeks=8)
        weekly = (
            apps.filter(applied_date__gte=since)
            .annotate(week=TruncWeek("applied_date"))
            .values("week")
            .annotate(count=Count("id"))
            .order_by("week")
        )

        # Funnel: how many applications EVER reached each stage (uses status history)
        def ever(status):
            return (
                StatusHistory.objects.filter(application__user=request.user, to_status=status)
                .values("application").distinct().count()
            )

        applied = by_status["applied"] + by_status["interview"] + by_status["offer"] + by_status["rejected"]
        interviews, offers = ever("interview"), ever("offer")
        pct = lambda a, b: round(100 * a / b, 1) if b else 0.0

        return Response({
            "total": apps.count(),
            "by_status": by_status,
            "weekly": [{"week": r["week"].isoformat(), "count": r["count"]} for r in weekly],
            "funnel": {
                "applied": applied,
                "interview": interviews,
                "offer": offers,
                "interview_rate": pct(interviews, applied),
                "offer_rate": pct(offers, applied),
            },
        })


class AdminStatsView(APIView):
    """Platform-wide stats, admin role only."""

    permission_classes = (IsAdminRole,)

    def get(self, request):
        User = get_user_model()
        return Response({
            "users": User.objects.count(),
            "applications": Application.objects.count(),
            "by_status": {
                r["status"]: r["n"]
                for r in Application.objects.values("status").annotate(n=Count("id"))
            },
        })
