# Django Imports
from django.db import models

# Own Imports
from apps.monitor.helpers.object_tracker import ObjectTracker


class Websites(ObjectTracker):
    """
    Defines the database schema for websites table in the database.

    Fields:
        - id (int): the object primary key
        - site (url): the url of the webite
        - has_authentication (bool): does the site require authentication?
        - date_created (datetime): the date and time the object was created
        - date_modified (datetime): the date and time the object was modified
    """

    site = models.URLField(unique=True)
    has_authentication = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.site)

    class Meta:
        db_table = "websites"
        verbose_name_plural = "Websites"


class AuthenticationSchema(ObjectTracker):
    """
    Defines the database schema for authentication schema table in the database.

    Fields:
        - id (int): the object primary key
        - date_created (datetime): the date and time the object was created
        - date_modified (datetime): the date and time the object was modified
    """

    def basic_auth_json_schema(cls) -> dict:
        return {"username": "", "password": ""}

    basic_auth = models.JSONField(
        default=basic_auth_json_schema, null=True, blank=True
    )
    bearer_auth = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self) -> str:
        if not self.bearer_auth:
            return self.basic_auth["username"]
        return self.bearer_auth

    class Meta:
        db_table = "authentication_schemas"
        verbose_name_plural = "Authentication Schemas"


class HistoricalStats(ObjectTracker):
    """
    Defines the database schema for historical_stats table in the database.

    Fields:
        - id (int): the object primary key
        - track (fk): foreign key relationship to the websites table
        - uptime_counts (int): the number of uptime counts
        - downtime_counts (int): the number of downtime counts
        - date_created (datetime): the date and time the object was created
        - date_modified (datetime): the date and time the object was modified
    """

    track = models.OneToOneField(Websites, on_delete=models.CASCADE)
    uptime_counts = models.PositiveBigIntegerField(default=0)
    downtime_counts = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.track.site}'s historical stats"

    class Meta:
        db_table = "historical_stats"
        verbose_name_plural = "Historial Stats"


class People(ObjectTracker):
    """
    Defines the database schema for people table in the database.

    Fields:
        - id (int): the object primary key
        - email_address (str): email address of the user
        - date_created (datetime): the date and time the object was created
        - date_modified (datetime): the date and time the object was modified
    """

    email_address = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.email_address

    class Meta:
        db_table = "people"
        verbose_name_plural = "People"


class NotifyGroup(ObjectTracker):
    """
    Defines the database schema for notify_group table in the database.

    Fields:
        - id (int): the object primary key
        - name (str): the name of the group to be notified
        - notify (fk): a foreign-key relationship to the websites table
        - emails (m2m): a many-to-many relationship to the people table
        - date_created (datetime): the date and time the object was created
        - date_modified (datetime): the date and time the object was modified
    """

    name = models.CharField(max_length=30, unique=True)
    notify = models.ForeignKey(Websites, on_delete=models.CASCADE)
    emails = models.ManyToManyField(People, related_name="people_notify_group")

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "notify_group"
        verbose_name_plural = "Notify Group"
