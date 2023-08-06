""" A client library for accessing Emby Server REST API (BETA) """
from .client import AuthenticatedClient, Client

__all__ = (
    "AuthenticatedClient",
    "Client",
)
