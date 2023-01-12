# Stdlib Imports
from typing import OrderedDict

# Django Imports
from django.db.transaction import atomic

# Rest Framework Imports
from rest_framework import serializers

# Own Imports
from apps.monitor.models import (
    HistoricalStats,
    Websites,
    AuthenticationScheme,
)


class AuthenticationSchemeSerializer(serializers.ModelSerializer):

    session_auth = serializers.JSONField(
        default={"username": "string", "password": "string"}, required=False
    )
    token_auth = serializers.CharField(required=False)
    bearer_auth = serializers.CharField(required=False)

    class Meta:
        model = AuthenticationScheme
        fields = ["session_auth", "token_auth", "bearer_auth"]


class WebsiteSerializer(serializers.ModelSerializer):

    auth_scheme = AuthenticationSchemeSerializer(required=False)

    class Meta:
        model = Websites
        fields = ["site", "auth_scheme"]

    @atomic
    def create(self, validated_data: OrderedDict) -> Websites:

        has_authentication = True if validated_data["auth_scheme"] else False

        # create authentication schema if website needs authentication
        if has_authentication:
            authentication_scheme = AuthenticationScheme.objects.get_or_create(
                site=validated_data["site"],
            )[0]

        try:
            session_auth = validated_data["auth_scheme"]["session_auth"]
            token_auth = validated_data["auth_scheme"]["token_auth"]
            bearer_auth = validated_data["auth_scheme"]["bearer_auth"]
        except (KeyError):
            token_auth = None
            bearer_auth = None

        # update authentication schema based on type
        if session_auth["username"] != "string":
            authentication_scheme.session_auth = session_auth

        elif token_auth is not None:
            authentication_scheme.token_auth = token_auth

        elif bearer_auth is not None:
            authentication_scheme.bearer_auth = bearer_auth

        # save authentication schema to database
        authentication_scheme.save()

        # return the newly created instance (website)
        return super().create(
            {
                "site": validated_data["site"],
                "auth_types": validated_data["auth_types"],
                "has_authentication": has_authentication,
            }
        )


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
