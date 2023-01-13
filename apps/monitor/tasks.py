# Stdlib Imports
from typing import List

# Django Imports
from django.conf import settings
from django.db import transaction
from django.core.mail import send_mail as send_mail_to_group, get_connection

# Own Imports
from apps.monitor.models import NotifyGroup, StatusTypes
from apps.monitor.selectors import get_historical_stats, get_website
from apps.monitor.tasks import notify_group_of_people_via_email

# Celery Imports
from celery import shared_task

# Third Import Imports
import httpx


@shared_task(max_retries=3)
def notify_group_of_people_via_email(website: str) -> str:
    """
    This function notifies a group of people via email when a website is down.

    :param website: str = The website that is currently facing a downtime
    :type website: str

    :return str: A message
    """

    group_emails = list(
        NotifyGroup.objects.filter(notify__site=website).values_list(
            "emails__email_address", flat=True
        )
    )

    mail_connection = get_connection(
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        fail_silently=True,
    )

    send_mail_to_group(
        subject="[NOTIFY]: Website downtime",
        message=f"Hello, {website} is currently facing a downtime.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=group_emails,
        connection=mail_connection,
    )

    return "Mail sent successfully!"


@transaction.atomic
@shared_task(max_tries=3)
def monitor_websites_up_x_downtimes(websites: List[str]) -> str:
    """
    This function checks if the website is up or down,
    and if it's down, it sends an email to a group of people.

    :param websites: List[str] -> This is the list of websites that we want to monitor
    :type websites: List[str]

    :return: A string of message.
    """

    with httpx.Client() as client:
        for website in websites:
            response, historial_stats = (
                client.get(website),
                get_historical_stats(website),
            )
            site, _ = get_website(website)

            if response.status_code == 200:

                # save up time to db
                historial_stats.uptime_counts += 1
                historial_stats.save(update_fields=["uptime_counts"])

                # update site uptime
                site.status = StatusTypes.UP
                site.save(update_fields=["status"])

                return "Uptime counts has increased with 1."

            elif response.status_code in [500, 502, 503, 504]:

                # save down time to db
                historial_stats.downtime_counts += 1
                historial_stats.save(update_fields=["downtime_counts"])

                # update site downtime
                site.status = StatusTypes.DOWN
                site.save(update_fields=["status"])

                # send mail to group
                notify_group_of_people_via_email.delay(website)
                return "Downtime counts has increased with 1."
