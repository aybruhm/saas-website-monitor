# Rest Framework Imports
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

# Own Imports
from apps.monitor.models import HistoricalStats, AuthTypes
from apps.monitor.serializers import (
    HistoricalStatsSerializer,
    WriteOnlyWebsiteSerializer,
    ReadOnlyWebsiteSerializer,
)
from apps.monitor.selectors import get_website
from apps.monitor.utils import validate_protocol


class AuthenticationTypesAPIView(generics.ListAPIView):
    def get(self, request: Request) -> Response:
        auth_types = AuthTypes.choices
        data = [{"name": auth[0]} for auth in auth_types]
        return Response(data=data, status=status.HTTP_200_OK)


class GetWebsiteAPIView(generics.RetrieveAPIView):

    serializer_class = ReadOnlyWebsiteSerializer

    def get(
        self, request: Request, protocol: str, domain_name: str
    ) -> Response:
        website = get_website(
            validate_protocol(protocol) + "://" + domain_name + "/"
        )
        serializer = self.serializer_class(website)

        return Response(
            {"message": "Website info retrieved!", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class AddWebsiteAPIView(generics.CreateAPIView):

    serializer_class = WriteOnlyWebsiteSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Website to monitor added!"},
            status=status.HTTP_201_CREATED,
        )


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
