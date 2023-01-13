# Stdlib Imports
from typing import OrderedDict, List

# Django Imports
from django.db.transaction import atomic

# Rest Framework Imports
from rest_framework import serializers

# Own Imports
from apps.monitor.models import (
    HistoricalStats,
    Websites,
    AuthTypes,
    AuthenticationScheme,
)
from apps.monitor.services import (
    session_authentication,
    token_authentication,
    bearer_authentication,
)


class AuthenticationSchemeSerializer(serializers.ModelSerializer):

    session_auth = serializers.CharField(required=False)
    token_auth = serializers.CharField(required=False)
    bearer_auth = serializers.CharField(required=False)

    class Meta:
        model = AuthenticationScheme
        fields = ["session_auth", "token_auth", "bearer_auth"]


class WriteOnlyWebsiteSerializer(serializers.ModelSerializer):

    auth_data = serializers.JSONField(
        default={"username": "string", "password": "string"}, required=False
    )
    auth_scheme = serializers.CharField(required=False)

    class Meta:
        model = Websites
        fields = ["site", "auth_data", "auth_scheme"]

    def get_authentication_schemes(self) -> List:
        return [scheme for scheme in AuthTypes.choices]

    @atomic
    def create(self, validated_data: OrderedDict) -> Websites:

        # get website from validated data
        website = validated_data["site"]

        try:
            authentication_scheme = validated_data["auth_scheme"]
        except (KeyError):
            authentication_scheme = None

        has_authentication = (
            True if authentication_scheme is not None else False
        )

        # create authentication schema if website needs authentication
        if has_authentication:
            authentication_scheme = AuthenticationScheme.objects.get_or_create(
                site=validated_data["site"],
            )[0]

        # update authentication schema based on type
        if validated_data["auth_scheme"] == "session":
            session_value = session_authentication(
                website,
                {
                    "username": validated_data["username"],
                    "password": validated_data["password"],
                },
            )
            authentication_scheme.session_auth = session_value

        elif validated_data["auth_scheme"] == "token":
            token_value = token_authentication(
                website,
                {
                    "username": validated_data["username"],
                    "password": validated_data["password"],
                },
            )
            authentication_scheme.token_auth = token_value

        elif validated_data["auth_scheme"] == "bearer":
            jwt_token = bearer_authentication(
                website,
                {
                    "username": validated_data["username"],
                    "password": validated_data["password"],
                },
            )
            authentication_scheme.bearer_auth = jwt_token

            # save authentication schema to database
            authentication_scheme.save()

        # return the newly created instance (website)
        return super().create(
            {
                "site": validated_data["site"],
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
