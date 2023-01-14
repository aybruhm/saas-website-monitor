# Stdlib Imports
from typing import OrderedDict, List

# Django Imports
from django.db.transaction import atomic
from django.contrib.auth.models import User

# Rest Framework Imports
from rest_framework import serializers, exceptions

# Own Imports
from apps.monitor.models import (
    HistoricalStats,
    Websites,
    AuthTypes,
    AuthenticationScheme,
    People,
    NotifyGroup,
)
from apps.monitor.selectors import get_website
from apps.monitor.services import Authentication


class AuthenticationSchemeSerializer(serializers.ModelSerializer):

    session_auth = serializers.CharField(required=False)
    token_auth = serializers.CharField(required=False)
    bearer_auth = serializers.CharField(required=False)

    class Meta:
        model = AuthenticationScheme
        fields = ["session_auth", "token_auth", "bearer_auth"]


class NotifyPeopleGroupSerializer(serializers.ModelSerializer):
    class PeopleSerializer(serializers.Serializer):
        email = serializers.EmailField(
            help_text="The email address of whom you want to add to group."
        )

    notify = serializers.URLField(
        help_text="Website to notify group of downtime."
    )
    emails = PeopleSerializer(many=True)

    class Meta:
        model = NotifyGroup
        fields = ["id", "name", "notify", "emails"]

    def create(self, validated_data: OrderedDict) -> NotifyGroup:

        # modifiy validated data
        data = validated_data
        data["notify"] = get_website(data["notify"])

        # list of people emails
        people_emails = []

        # create people emails
        for email_data in data["emails"]:
            people, _ = People.objects.get_or_create(
                email_address=email_data["email"]
            )
            people.save(update_fields=["email_address"])

            # append people to list
            people_emails.append(people)

        # create group to notify
        notify_group = NotifyGroup.objects.create(
            name=data["name"], notify=data["notify"]
        )

        # set people emails and save to database
        notify_group.emails.set(people_emails)
        notify_group.save()

        return notify_group


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


class ReadOnlyWebsiteSerializer(serializers.ModelSerializer):

    historical_data = serializers.SerializerMethodField()

    class OwnHistoricalStatsSerializer(serializers.ModelSerializer):
        class Meta:
            model = HistoricalStats
            fields = [
                "uptime_counts",
                "downtime_counts",
                "date_created",
                "date_modified",
            ]
            read_only_fields = fields

    class Meta:
        model = Websites
        fields = [
            "id",
            "site",
            "status",
            "has_authentication",
            "historical_data",
        ]
        read_only_fields = fields

    def get_historical_data(self, obj: Websites) -> dict:
        historical_data = HistoricalStats.objects.filter(
            track__site=obj.site
        ).first()
        return self.OwnHistoricalStatsSerializer(historical_data).data


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

            # initialize the authentication service
            auth_service = Authentication(
                website,
                validated_data["auth_data"]["username"],
                validated_data["auth_data"]["password"],
            )

            # update authentication schema based on type
            if validated_data["auth_scheme"] == "session":
                session_value = auth_service.authenticate_with_session()
                authentication_scheme.session_auth = session_value

            elif validated_data["auth_scheme"] == "token":
                token_value = auth_service.authenticate_with_token()
                authentication_scheme.token_auth = token_value

            elif validated_data["auth_scheme"] == "bearer":
                jwt_token_value = auth_service.authenticate_with_jwt()
                authentication_scheme.bearer_auth = jwt_token_value

            # save authentication schema to database
            authentication_scheme.save()

        # return the newly created instance (website)
        return super().create(
            {
                "site": validated_data["site"],
                "has_authentication": has_authentication,
            }
        )


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise exceptions.NotFound({"message": "User does exist!"})
        return value

    def create(self, validated_data: OrderedDict) -> User:

        user = User.objects.create(**dict(validated_data))
        user.set_password(validated_data["password"])
        user.save()

        return user


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
