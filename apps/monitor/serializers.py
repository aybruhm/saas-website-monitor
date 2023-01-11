# Stdlib Imports
from typing import OrderedDict

# Rest Framework Imports
from rest_framework import serializers

# Own Imports
from apps.monitor.models import HistoricalStats, Websites, AuthTypes


class WebsiteSerializer(serializers.ModelSerializer):

    auth_types = serializers.CharField(required=False, default="basic")
    has_authentication = serializers.BooleanField(default=False)

    class Meta:
        model = Websites
        fields = ["site", "auth_types", "has_authentication"]

    def validate_auth_types(self, value: str) -> str:
        auth_types = [auth[0] for auth in AuthTypes.choices]

        if value not in auth_types:
            raise serializers.ValidationError(
                {"message": "Authentication type not supported."}
            )
        return value

    def _ensure_auth_types_requires_authentication_flag(
        self, authenticated: bool, auth_type: str
    ):
        if authenticated and not auth_type:
            raise serializers.ValidationError(
                {"message": "Authentication type is required."}
            )

        if not authenticated and auth_type is not None:
            raise serializers.ValidationError(
                {"message": "Authentication needs to be set."}
            )

    def create(self, validated_data: OrderedDict) -> Websites:
        # validation to ensure that auth types
        # requires authentication to be True
        self._ensure_auth_types_requires_authentication_flag(
            validated_data["has_authentication"],
            validated_data["auth_types"],
        )
        return super().create(validated_data)


class HistoricalStatsSerializer(serializers.ModelSerializer):

    track = serializers.CharField(source="track.site")

    class Meta:
        model = HistoricalStats
        fields = [
            "id",
            "track",
            "uptime_counts",
            "downtime_counts",
            "date_created",
            "date_modified",
        ]
        read_only_fields = fields
