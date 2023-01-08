# Rest Framework Imports
from rest_framework import exceptions

# Own Imports
from apps.monitor.models import HistoricalStats


def get_historical_stats(website: str) -> HistoricalStats:
    """
    This function gets the historical stats for a website.
    
    :param website: str
    :type website: str
    
    :return: The historical stats for a website.
    """
    
    try:
        historial_stats = HistoricalStats.objects.get(
            track__site=website
        ).first()
        return historial_stats
    except (HistoricalStats.DoesNotExist):
        raise exceptions.NotFound(
            {"message": "Historial stats for website not found."}
        )
