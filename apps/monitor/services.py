# Stdlib Imports
from typing import List

# Django Imports
from django.db import transaction

# Own Imports
from apps.monitor.utils import (
    get_historical_stats,
    notify_group_of_people_via_email,
)

# Third Party Imports
import httpx


@transaction.atomic
def monitor_websites(websites: List[str]) -> str:
    """
    This function checks if the website is up or down,
    and if it's down, it sends an email to a group of people.

    :param websites: List[str] -> This is the list of websites that we want to monitor
    :type websites: List[str]

    :return: A string of message.
    """

    with httpx.Client() as client:
        for website in websites:
            response, historial_stats = client.get(
                website
            ), get_historical_stats(website)

            if response.status_code == 200:

                # save up time to db
                historial_stats.uptime_counts += 1
                historial_stats.save(update_fields=["uptime_counts"])
                return "Uptime counts has increased with 1."

            elif response.status_code in [500, 502, 503, 504]:

                # save down time to db
                historial_stats.downtime_counts += 1
                historial_stats.save(update_fields=["downtime_counts"])

                # send mail to group
                notify_group_of_people_via_email(website)
                return "Downtime counts has increased with 1."
