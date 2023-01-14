# Django Imports
from django.urls import path, include

# Own Imports
from apps.monitor.views import (
    AuthenticationTypesAPIView,
    AddWebsiteAPIView,
    AddNotifyGroupAPIView,
    GetLogsOfHistoricalStatsAPIView,
    GetWebsiteAPIView,
    # auth imports
    RegisterUserAPIView,
    LoginUserAPIView,
    LogoutUserAPIView,
)


app_name = "monitor"


auth_routes = [
    path("register/", RegisterUserAPIView.as_view(), name="register_user"),
    path("login/", LoginUserAPIView.as_view(), name="login_user"),
    path("logout/", LogoutUserAPIView.as_view(), name="logout_user"),
]

urlpatterns = [
    path(
        "authentication-types/",
        AuthenticationTypesAPIView.as_view(),
        name="auth_types",
    ),
    path("add-website/", AddWebsiteAPIView.as_view(), name="add_website"),
    path("add-notify-group/", AddNotifyGroupAPIView.as_view(), name="add_notify_group"),
    path(
        "get-website/<str:protocol>/<str:domain_name>/",
        GetWebsiteAPIView.as_view(),
        name="get_website"
    ),
    path(
        "historical-stats/",
        GetLogsOfHistoricalStatsAPIView.as_view(),
        name="historical_stats",
    ),
    # auth include
    path("auth/", include(auth_routes)),
]
