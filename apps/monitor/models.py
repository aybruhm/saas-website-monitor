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
        - date_created (datetime): the date and time the object was created
        - date_modified (datetime): the date and time the object was modifieds
    """

    site = models.URLField(unique=True)

    def __str__(self) -> str:
        return str(self.site)

    class Meta:
        db_table = "websites"
        verbose_name_plural = "Websites"


class HistoricalStats(ObjectTracker):
    """
    Defines the database schema for historical_stats table in the database.

    Fields:
        - id (int): the object primary key
        - track (fk): foreign key relationship to the websites table
        - up_counts (int): the number of uptime counts
        - down_counts (int): the number of downtime counts
        - date_created (datetime): the date and time the object was created
        - date_modified (datetime): the date and time the object was modifieds
    """

    track = models.ForeignKey(Websites, on_delete=models.CASCADE)
    up_counts = models.PositiveBigIntegerField(default=0)
    down_counts = models.PositiveBigIntegerField(default=0)

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
        - date_modified (datetime): the date and time the object was modifieds
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
        - emails (m2m): a many-to-many relationship to the people table
        - date_created (datetime): the date and time the object was created
        - date_modified (datetime): the date and time the object was modifieds
    """

    name = models.CharField(max_length=30, unique=True)
    emails = models.ManyToManyField(People, related_name="people_notify_group")

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "Notify Group"
        verbose_name_plural = "Notify Group"
