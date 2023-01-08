# Django Imports
from django.conf import settings
from django.core.mail import send_mail as send_mail_to_group

# Own Imports
from apps.monitor.models import Websites, HistoricalStats, NotifyGroup


def get_historical_stats(website: str) -> HistoricalStats:
    """
    This function gets the historical stats for a website,
    or creates one if it doesn't exist.

    :param website: str
    :type website: str

    :return: A HistoricalStats object
    """

    try:
        historial_stats = HistoricalStats.objects.get(track__site=website)
    except (HistoricalStats.DoesNotExist):
        historial_stats = HistoricalStats.objects.create(
            track=Websites.objects.get_or_create(site=website)[0]
        )
        historial_stats.save(update_fields=["track"])

    return historial_stats


def notify_group_of_people_via_email(website: str):
    """
    This function notifies a group of people via email when a website is down.

    :param website: str = The website that is currently facing a downtime
    :type website: str
    """

    group_emails = list(
        NotifyGroup.objects.filter(notify__site=website).values_list(
            "emails__email_address", flat=True
        )
    )

    send_mail_to_group(
        subject="[NOTIFY]: Website downtime",
        message=f"Hello, {website} is currently facing a downtime.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=group_emails,
        fail_silently=True,
    )
