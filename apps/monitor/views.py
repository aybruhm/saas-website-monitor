# Rest Framework Imports
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

# Own Imports
from apps.monitor.models import HistoricalStats
from apps.monitor.serializers import HistoricalStatsSerializer


class GetLogsOfHistoricalStatsAPIView(generics.GenericAPIView):

    serializer_class = HistoricalStatsSerializer
    queryset = HistoricalStats.objects.select_related("track")

    def get(self, request: Request) -> Response:
        historical_stats = self.get_queryset()
        serializer = self.serializer_class(historical_stats, many=True)
        return Response(
            {
                "message": "Log of historical stats retrieved!",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
