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