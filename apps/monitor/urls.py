# Django Imports
from django.urls import path

# Own Imports
from apps.monitor.views import (
    AuthenticationTypesAPIView,
    AddWebsiteAPIView,
    GetLogsOfHistoricalStatsAPIView,
)


app_name = "monitor"

urlpatterns = [
    path(
        "authentication-types/",
        AuthenticationTypesAPIView.as_view(),
        name="auth_types",
    ),
    path("add-website/", AddWebsiteAPIView.as_view(), name="add_website"),
    path(
        "historical-stats/",
        GetLogsOfHistoricalStatsAPIView.as_view(),
        name="historical_stats",
    ),
]
