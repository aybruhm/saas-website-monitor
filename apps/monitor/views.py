# Rest Framework Imports
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

# Own Imports
from apps.monitor.models import HistoricalStats, AuthTypes
from apps.monitor.serializers import (
    HistoricalStatsSerializer,
    WebsiteSerializer,
)


class AuthenticationTypesAPIView(generics.ListAPIView):
    def get(self, request: Request) -> Response:
        auth_types = AuthTypes.choices
        data = [{"name": auth[0]} for auth in auth_types]
        return Response(data=data, status=status.HTTP_200_OK)


class AddWebsiteAPIView(generics.CreateAPIView):

    serializer_class = WebsiteSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "message": "Website to monitor added!",
            "data": serializer.data,
        }
        return Response(data=response, status=status.HTTP_201_CREATED)


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
