from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.connect_user_link_result import ConnectUserLinkResult
from ...types import UNSET, Response


def _get_kwargs(
    id: str,
    *,
    client: AuthenticatedClient,
    connect_username: str,
) -> Dict[str, Any]:
    url = "{}/Users/{Id}/Connect/Link".format(client.base_url, Id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ConnectUsername"] = connect_username

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, ConnectUserLinkResult]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ConnectUserLinkResult.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, ConnectUserLinkResult]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    connect_username: str,
) -> Response[Union[Any, ConnectUserLinkResult]]:
    """Creates a Connect link for a user

     Requires authentication as administrator

    Args:
        id (str):
        connect_username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConnectUserLinkResult]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        connect_username=connect_username,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    connect_username: str,
) -> Optional[Union[Any, ConnectUserLinkResult]]:
    """Creates a Connect link for a user

     Requires authentication as administrator

    Args:
        id (str):
        connect_username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConnectUserLinkResult]
    """

    return sync_detailed(
        id=id,
        client=client,
        connect_username=connect_username,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    connect_username: str,
) -> Response[Union[Any, ConnectUserLinkResult]]:
    """Creates a Connect link for a user

     Requires authentication as administrator

    Args:
        id (str):
        connect_username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConnectUserLinkResult]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        connect_username=connect_username,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    connect_username: str,
) -> Optional[Union[Any, ConnectUserLinkResult]]:
    """Creates a Connect link for a user

     Requires authentication as administrator

    Args:
        id (str):
        connect_username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConnectUserLinkResult]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            connect_username=connect_username,
        )
    ).parsed
