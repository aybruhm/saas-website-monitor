# Django Imports
from django.db import models

# Own Imports
from apps.monitor.helpers.object_tracker import ObjectTracker


class AuthTypes(models.Choices):
    SESSION_AUTH = "session"
    TOKEN_AUTH = "token"
    JWT_AUTH = "bearer"


class StatusTypes(models.Choices):
    UP = "up"
    DOWN = "down"


class Websites(ObjectTracker):
    """
    Defines the schema for websites table in the database.

    Fields:
        - id (int): the object primary key
        - site (url): the url of the webite
        - status (str): the status (up, down) of the website
        - has_authentication (bool): does the site require authentication?
        - date_created (datetime): the date and time the object was created
        - date_modified (datetime): the date and time the object was modified
    """

    site = models.URLField(unique=True)
    status = models.CharField(
        max_length=4, choices=StatusTypes.choices, null=True, blank=True
    )
    has_authentication = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.site)

    class Meta:
        db_table = "websites"
        ordering = ["-date_created"]
        verbose_name_plural = "Websites"


class AuthenticationScheme(ObjectTracker):
    """
    Defines the schema for authentication scheme table in the database.

    Fields:
        - id (int): the object primary key
        - session_auth (str): session authentication (requires username and password)
        - token_auth (str): token authentication (x-api-key, token)
        - bearer_auth (str): jwt authentication (jwt, bearer)
        - date_created (datetime): the date and time the object was created
        - date_modified (datetime): the date and time the object was modified
    """

    site = models.URLField(unique=True)
    session_auth = models.CharField(max_length=300, null=True, blank=True)
    token_auth = models.CharField(max_length=300, null=True, blank=True)
    bearer_auth = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.site}'s authentication scheme"

    class Meta:
        db_table = "authentication_schemes"
        ordering = ["-date_created"]
        verbose_name_plural = "Authentication Schemes"


class HistoricalStats(ObjectTracker):
    """
    Defines the schema for historical stats table in the database.

    Fields:
        - id (int): the object primary key
        - track (o2o): one-two-one key relationship to the websites table
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
        ordering = ["-date_created"]
        verbose_name_plural = "Historial Stats"


class People(ObjectTracker):
    """
    Defines the schema for people table in the database.

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
        ordering = ["-date_created"]
        verbose_name_plural = "People"


class NotifyGroup(ObjectTracker):
    """
    Defines the schema for notify group table in the database.

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
        ordering = ["-date_created"]
        verbose_name_plural = "Notify Group"
