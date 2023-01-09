# Rest Framework Imports
from rest_framework import serializers

# Own Imports
from apps.monitor.models import HistoricalStats


class HistoricalStatsSerializer(serializers.ModelSerializer):

    track = serializers.CharField(source="track.site")

    class Meta:
        model = HistoricalStats
        fields = [
            "id",
            "track",
            "uptime_counts",
            "downtime_counts",
            "date_created",
            "date_modified",
        ]
        read_only_fields = fields
