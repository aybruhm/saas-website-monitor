# Third Party Imports
import httpx


def session_authentication(website: str, data: dict) -> dict:
    """
    This function takes a website and a dictionary of data,
    and returns the cookies from the response.

    :param website: The website you want to authenticate to
    :type website: str

    :param data: The data that you want to send to the website
    :type data: dict

    :return: A dictionary of cookies
    """

    auth_data = {"username": data["username"], "password": data["password"]}
    response = httpx.post(website, data=auth_data)
    return response.cookies


def token_authentication(website: str, data: dict) -> str:
    """
    This function takes in a website and a dictionary of data, and returns a token.

    :param website: The website you want to authenticate with
    :type website: str

    :param data: This is the data that you want to send to the server
    :type data: dict

    :return: The token is being returned.
    """

    auth_data = {"username": data["username"], "password": data["password"]}
    response = httpx.post(website, data=auth_data)

    try:
        token = response.json()["data"]["token"]
    except (KeyError):
        token = response.json()["token"]
    return token


def bearer_authentication(website: str, data: dict) -> str:
    """
    This function takes a website and a dictionary of data, and returns a JWT token.

    :param website: The website you want to authenticate with
    :type website: str

    :param data: This is the data that you want to send to the website
    :type data: dict

    :return: A JWT token.
    """

    auth_data = {"username": data["username"], "password": data["password"]}
    response = httpx.post(website, data=auth_data)

    try:
        jwt_token = response.json()["data"]["access"]
    except (KeyError):
        jwt_token = response.json()["access"]
    return jwt_token

