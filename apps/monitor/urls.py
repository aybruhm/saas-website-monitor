# Django Imports
from django.urls import reverse, path

# Own Imports
from apps.monitor.views import GetLogsOfHistoricalStatsAPIView


app_name = "monitor"

urlpatterns = [
    path(
        "historical-stats/",
        GetLogsOfHistoricalStatsAPIView.as_view(),
        name="historical_stats",
    )
]
