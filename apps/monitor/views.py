# Rest Framework Imports
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, status, exceptions, permissions

# Django Imports
from django.contrib.auth import authenticate, login, logout

# Own Imports
from apps.monitor.models import HistoricalStats, AuthTypes
from apps.monitor.serializers import (
    HistoricalStatsSerializer,
    WriteOnlyWebsiteSerializer,
    ReadOnlyWebsiteSerializer,
    CreateUserSerializer,
    LoginUserSerializer,
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
    permission_classes = (permissions.IsAuthenticated,)

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


class RegisterUserAPIView(generics.CreateAPIView):

    serializer_class = CreateUserSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "User created successful!"},
            status=status.HTTP_201_CREATED,
        )


class LoginUserAPIView(generics.CreateAPIView):

    serializer_class = LoginUserSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            raise exceptions.NotFound(
                {"message": "User credentials not found!"}
            )

        login(request, user)
        return Response(
            {"message": "Login successful!"}, status=status.HTTP_200_OK
        )


class LogoutUserAPIView(generics.CreateAPIView):
    def post(self, request: Request) -> Response:
        logout(request)
        return Response(
            {"message": "User logout successful!"}, status=status.HTTP_200_OK
        )
