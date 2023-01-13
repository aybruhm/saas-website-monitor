# Rest Framework Imports
from rest_framework import exceptions


def validate_protocol(protocol: str) -> str:
    """
    This function checks if the protocol is not https or http,
    otherwise raise a validation error.

    :param protocol: The protocol to use for the connection
    :type protocol: str

    :return: The protocol is being returned.
    """

    if protocol not in ["https", "http"]:
        raise exceptions.ValidationError(
            {"message": "Protocol is not supported."}
        )
    return protocol
