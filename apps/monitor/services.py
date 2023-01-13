# Third Party Imports
import httpx


# This class is used to authenticate with a website
class Authentication:
    """
    This class service is responsible for authenticating a website, with:

    - session authentication
    - token authentication
    - jwt authentication
    """

    def __init__(self, website: str, username: str, password: str) -> None:
        self.website = website
        self.username = username
        self.password = password

    def authenticate_with_session(self) -> dict:
        """
        This method takes no arguments and returns a dictionary of cookies.

        :return: A dictionary of cookies.
        """

        auth_data = {"username": self.username, "password": self.password}
        response = httpx.post(self.website, data=auth_data)
        return response.cookies

    def authenticate_with_token(self) -> str:
        """
        This method takes in a username and password and returns a token.

        :return: The token is being returned.
        """

        auth_data = {"username": self.username, "password": self.password}
        response = httpx.post(self.website, data=auth_data, format="json")

        try:
            token = response.json()["data"]["token"]
        except (KeyError):
            token = response.json()["token"]
        return token

    def authenticate_with_jwt(self) -> str:
        """
        This method takes the username and password from the class and
        uses them to authenticate with the website.

        :return: A JWT token.
        """

        auth_data = {"username": self.username, "password": self.password}
        response = httpx.post(self.website, data=auth_data, format="json")

        try:
            jwt_token = response.json()["data"]["access"]
        except (KeyError):
            jwt_token = response.json()["access"]
        return jwt_token
