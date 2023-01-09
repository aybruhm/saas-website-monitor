# Django Imports
from django.conf import settings
from django.core.mail import send_mail as send_mail_to_group, get_connection

# Own Imports
from apps.monitor.models import NotifyGroup

# Celery Imports
from celery import shared_task


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
