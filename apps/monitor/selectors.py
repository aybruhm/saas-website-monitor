# Rest Framework Imports
from rest_framework import exceptions

# Own Imports
from apps.monitor.models import Websites, HistoricalStats


def get_website(site: str) -> Websites:
    """
    This function takes in a site, checks if the site requires
    authentication; if it does return the site and a True bool,
    otherwise return the site and a False bool.

    :param site: The website you want to get the authentication status of
    :type site: str

    :return: The website and a boolean value.
    """

    try:
        website = Websites.objects.get(site=site)
    except (Websites.DoesNotExist):
        raise exceptions.NotFound({"message": "Website does not exist!"})

    return website


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
