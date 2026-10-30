from django.urls import path

from .views import AdminStatsView, SummaryView

urlpatterns = [
    path("summary/", SummaryView.as_view(), name="summary"),
    path("admin-stats/", AdminStatsView.as_view(), name="admin-stats"),
]
