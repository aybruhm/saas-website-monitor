# Rest Framework Imports
from rest_framework.test import APIClient, APITestCase

# Django Imports
from django.urls import reverse
from django.contrib.auth.models import User

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

        self.user = User.objects.create(
            email="user.test@test.com",
            username="user.test",
            password="user.test",
        )
        self.user.set_password("user.test")
        self.user.save()

        self.no_auth_payload = {"site": "http://testserver.com"}
        self.session_auth_payload = {
            "site": "http://127.0.0.1:8000/api/login/",
            "auth_data": {
                "username": self.user.username,
                "password": "user.test",
            },
            "auth_scheme": "session",
        }
        self.token_auth_payload = {
            "site": "http://testserver.com",
            "auth_data": {"username": "string", "password": "string"},
            "auth_scheme": "token",
        }
        self.bearer_auth_payload = {
            "site": "http://testserver.com",
            "auth_data": {"username": "string", "password": "string"},
            "auth_scheme": "bearer",
        }

    def test_add_website_with_no_authentication(self):
        """Ensure that we can add a website that has not authentication."""

        url = reverse("monitor:add_website")
        response = client.post(url, data=self.no_auth_payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["message"], "Website to monitor added!"
        )

    def test_add_website_with_session_authentication(self):
        """Ensure that we can add a website that has session authentication."""

        url = reverse("monitor:add_website")
        response = client.post(
            url, data=self.session_auth_payload, format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["message"], "Website to monitor added!"
        )

    def test_add_website_with_token_authentication(self):
        """Ensure that we can add a website that has token authentication."""

        url = reverse("monitor:add_website")

        ...

    def test_add_website_with_bearer_authentication(self):
        """Ensure that we can add a website that has jwt authentication."""

        url = reverse("monitor:add_website")

        ...


class GetLogsOfHistoricalStatsTestCase(APITestCase):
    """Test case for get logs of historical stats api view."""

    def setUp(self) -> None:
        """Setup fixtutes for get logs of historical stats test case."""

        self.user = User.objects.create(
            email="user.test@test.com",
            username="user.test",
            password="user.test",
        )
        self.user.set_password("user.test")
        self.user.save()

        self.website = Websites.objects.create(site="http://127.0.0.1:8000/")
        self.historical_stats = HistoricalStats.objects.create(
            track=self.website
        )

    def test_unauthenticated_get_logs_of_historical_stats(self):
        """
        Ensure that we can get a list of historical stats logs,
        and the request is not authenticated.
        """

        url = reverse("monitor:historical_stats")

        client.logout()
        response = client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_authenticated_get_logs_of_historical_stats(self):
        """
        Ensure that we can get a list of historical stats logs,
        and the request is authenticated.
        """

        url = reverse("monitor:historical_stats")

        client.force_authenticate(self.user)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"], "Log of historical stats retrieved!"
        )
        self.assertEqual(len(response.json()["data"]), 1)


class RegisterUserTestCase(APITestCase):
    """Test case for register user api view."""

    def setUp(self) -> None:
        """Setup fixtures for register user test case."""

        self.payload = {
            "email": "user@example.com",
            "username": "string",
            "password": "string",
        }

    def test_register_user(self):
        """Ensure that we can register a new user."""

        url = reverse("monitor:register_user")
        response = client.post(url, data=self.payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["message"], "User created successful!"
        )


class LoginUserTestCase(APITestCase):
    """Test case for login user api view."""

    def setUp(self) -> None:
        """Setup fixtures for login user test case."""

        self.user = User.objects.create(
            email="user.test@test.com",
            username="user.test",
            password="user.test",
        )
        self.user.set_password("user.test")
        self.user.save()

        self.payload = {
            "username": self.user.username,
            "password": "user.test",
        }

    def test_login_user(self):
        """Ensure that we can login a user."""

        url = reverse("monitor:login_user")
        response = client.post(url, data=self.payload, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Login successful!")


class LogoutUserTestCase(APITestCase):
    """Test case for logout user api view."""

    def test_logout_user(self):
        """Ensure that a user can logout."""

        url = reverse("monitor:logout_user")
        response = client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User logout successful!")
