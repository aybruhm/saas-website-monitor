# Rest Framework Imports
from rest_framework.test import APIClient, APITestCase

# Django Imports
from django.urls import reverse

# Own Imports
from apps.monitor.models import Websites, HistoricalStats


# initialize api client
client = APIClient()


class AuthenticationTypesTestCase(APITestCase):
    """Test case for authentication types api view."""

    def test_authentication_types_are_valid(self):
        """Ensure that the authentication types are valid."""

        url = reverse("monitor:auth_types")
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"name": "session"}, {"name": "token"}, {"name": "bearer"}],
        )


class GetWebsitesTestCase(APITestCase):
    """Test case for get websites api view."""

    def setUp(self) -> None:
        """Setup fixtures for get websites test case."""

        self.website = Websites.objects.create(site="http://127.0.0.1:8000/")
        self.historical_stats = HistoricalStats.objects.create(
            track=self.website
        )

    def test_get_websites_api_works(self):
        """Ensure that getting a website works."""

        url = reverse("monitor:get_website", args=["http", "127.0.0.1:8000"])
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Website info retrieved!")
        self.assertEqual(response.json()["data"]["site"], self.website.site)


class AddWebsiteTestCase(APITestCase):
    """Test case for add website api view."""

    def setUp(self) -> None:
        """Setup fixtures for adding websites test case."""

        self.no_auth_payload = {"site": "http://testserver"}
        self.session_auth_payload = {
            "site": "string",
            "auth_data": {"username": "string", "password": "string"},
            "auth_scheme": "session",
        }
        self.token_auth_payload = {
            "site": "string",
            "auth_data": {"username": "string", "password": "string"},
            "auth_scheme": "token",
        }
        self.bearer_auth_payload = {
            "site": "string",
            "auth_data": {"username": "string", "password": "string"},
            "auth_scheme": "bearer",
        }

    def test_add_website_with_no_authentication(self):
        """Ensure that we can add a website that has not authentication."""

        url = reverse("monitor:add_website")
        response = client.post(url, data=self.payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["message"], "Website to monitor added!"
        )
