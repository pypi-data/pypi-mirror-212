from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    name: str,
    description: str,
    image_url: Union[Unset, None, str] = UNSET,
    url: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/Notifications/Admin".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["Name"] = name

    params["Description"] = description

    params["ImageUrl"] = image_url

    params["Url"] = url

    params["Level"] = level

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        return None
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        return None
    if response.status_code == HTTPStatus.FORBIDDEN:
        return None
    if response.status_code == HTTPStatus.NOT_FOUND:
        return None
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    name: str,
    description: str,
    image_url: Union[Unset, None, str] = UNSET,
    url: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Sends a notification to all admin users

     Requires authentication as user

    Args:
        name (str):
        description (str):
        image_url (Union[Unset, None, str]):
        url (Union[Unset, None, str]):
        level (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        name=name,
        description=description,
        image_url=image_url,
        url=url,
        level=level,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    name: str,
    description: str,
    image_url: Union[Unset, None, str] = UNSET,
    url: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Sends a notification to all admin users

     Requires authentication as user

    Args:
        name (str):
        description (str):
        image_url (Union[Unset, None, str]):
        url (Union[Unset, None, str]):
        level (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        name=name,
        description=description,
        image_url=image_url,
        url=url,
        level=level,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
