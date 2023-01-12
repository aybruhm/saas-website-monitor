# Stdlib Imports
from typing import List

# Django Imports
from django.db import transaction

# Own Imports
from apps.monitor.selectors import get_historical_stats
from apps.monitor.tasks import notify_group_of_people_via_email

# Third Party Imports
import httpx


def session_authentication(website: str, data: dict) -> dict:
    """
    This function takes a website and a dictionary of data,
    and returns the cookies from the response.

    :param website: The website you want to authenticate to
    :type website: str

    :param data: The data that you want to send to the website
    :type data: dict

    :return: A dictionary of cookies
    """

    auth_data = {"username": data["username"], "password": data["password"]}
    response = httpx.post(website, data=auth_data)
    return response.cookies


def token_authentication(website: str, data: dict) -> str:
    """
    This function takes in a website and a dictionary of data, and returns a token.

    :param website: The website you want to authenticate with
    :type website: str

    :param data: This is the data that you want to send to the server
    :type data: dict

    :return: The token is being returned.
    """

    auth_data = {"username": data["username"], "password": data["password"]}
    response = httpx.post(website, data=auth_data)

    try:
        token = response.json()["data"]["token"]
    except (KeyError):
        token = response.json()["token"]
    return token


def bearer_authentication(website: str, data: dict) -> str:
    """
    This function takes a website and a dictionary of data, and returns a JWT token.

    :param website: The website you want to authenticate with
    :type website: str

    :param data: This is the data that you want to send to the website
    :type data: dict

    :return: A JWT token.
    """

    auth_data = {"username": data["username"], "password": data["password"]}
    response = httpx.post(website, data=auth_data)

    try:
        jwt_token = response.json()["data"]["access"]
    except (KeyError):
        jwt_token = response.json()["access"]
    return jwt_token


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
                notify_group_of_people_via_email.delay(website)
                return "Downtime counts has increased with 1."
