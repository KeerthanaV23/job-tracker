from django.urls import path

from .views import AnalysisListView, AnalyzeView

urlpatterns = [
    path("analyze/", AnalyzeView.as_view(), name="analyze"),
    path("", AnalysisListView.as_view(), name="analysis-list"),
]
