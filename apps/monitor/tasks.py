# Django Imports
from django.conf import settings
from django.db import transaction
from django.core.mail import send_mail as send_mail_to_group, get_connection

# Own Imports
from apps.monitor.models import (
    NotifyGroup,
    StatusTypes,
    Websites,
    AuthenticationScheme,
)
from apps.monitor.selectors import get_historical_stats, get_website

# Celery Imports
from celery import shared_task

# Third Import Imports
import httpx


@shared_task(name="notify_group_of_people_via_email", max_retries=3)
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


@shared_task(name="monitor_websites_up_and_downtimes", max_tries=3)
def monitor_websites_up_and_downtimes() -> str:
    """
    This function checks if the website is up or down,
    and if it's down, it sends an email to a group of people.

    :return: A string of message.
    """

    with transaction.atomic():
        # wrap query in an atomic transaction

        with httpx.Client() as client:
            for website in list(
                Websites.objects.values_list("site", flat=True)
            ):

                # get the historical stats of the
                # website and the site object
                site = get_website(website)
                historical_stats = get_historical_stats(website)

                # if site does not has authentication,
                # get the response of the website without
                # no authentication scheme
                if not site.has_authentication:
                    response = client.get(website)

                elif site.has_authentication:

                    # get the authentication scheme of the website
                    authentication_scheme = AuthenticationScheme.objects.get(
                        site=website
                    )

                    # get the response of the website based on the session
                    if authentication_scheme.session_auth is not None:
                        response = client.get(
                            website, cookies=authentication_scheme.session_auth
                        )

                    # get the response of the website based on the token
                    elif authentication_scheme.token_auth is not None:
                        response = client.get(
                            website,
                            headers={
                                "Authorization": f"Token {authentication_scheme.token_auth}"
                            },
                        )

                    # get the response of the website based on the bearer
                    elif authentication_scheme.bearer_auth is not None:
                        response = client.get(
                            website,
                            headers={
                                "Authorization": f"Bearer {authentication_scheme.bearer_auth}"
                            },
                        )
                        print('Response: ', response.json())

                if response.status_code == 200:

                    # save up time to db
                    historical_stats.uptime_counts += 1
                    historical_stats.save(update_fields=["uptime_counts"])

                    # update site uptime
                    site.status = StatusTypes.UP
                    site.save(update_fields=["status"])

                    print(f"Uptime counts for {website} has increased with 1.")

                elif response.status_code in [500, 502, 503, 504]:

                    # save down time to db
                    historical_stats.downtime_counts += 1
                    historical_stats.save(update_fields=["downtime_counts"])

                    # update site downtime
                    site.status = StatusTypes.DOWN
                    site.save(update_fields=["status"])

                    # send mail to group
                    notify_group_of_people_via_email.delay(website)
                    print(
                        f"Downtime counts for {website} has increased with 1."
                    )

            return "Monitoring done!"
