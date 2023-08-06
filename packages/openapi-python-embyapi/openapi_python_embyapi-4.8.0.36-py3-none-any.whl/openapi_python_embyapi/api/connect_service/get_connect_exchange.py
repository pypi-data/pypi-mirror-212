from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.connect_connect_authentication_exchange_result import ConnectConnectAuthenticationExchangeResult
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    connect_user_id: str,
) -> Dict[str, Any]:
    url = "{}/Connect/Exchange".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ConnectUserId"] = connect_user_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[Any, ConnectConnectAuthenticationExchangeResult]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ConnectConnectAuthenticationExchangeResult.from_dict(response.json())

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


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, ConnectConnectAuthenticationExchangeResult]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    connect_user_id: str,
) -> Response[Union[Any, ConnectConnectAuthenticationExchangeResult]]:
    """Gets the corresponding local user from a connect user id

     Requires authentication as user

    Args:
        connect_user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConnectConnectAuthenticationExchangeResult]]
    """

    kwargs = _get_kwargs(
        client=client,
        connect_user_id=connect_user_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    connect_user_id: str,
) -> Optional[Union[Any, ConnectConnectAuthenticationExchangeResult]]:
    """Gets the corresponding local user from a connect user id

     Requires authentication as user

    Args:
        connect_user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConnectConnectAuthenticationExchangeResult]
    """

    return sync_detailed(
        client=client,
        connect_user_id=connect_user_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    connect_user_id: str,
) -> Response[Union[Any, ConnectConnectAuthenticationExchangeResult]]:
    """Gets the corresponding local user from a connect user id

     Requires authentication as user

    Args:
        connect_user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConnectConnectAuthenticationExchangeResult]]
    """

    kwargs = _get_kwargs(
        client=client,
        connect_user_id=connect_user_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    connect_user_id: str,
) -> Optional[Union[Any, ConnectConnectAuthenticationExchangeResult]]:
    """Gets the corresponding local user from a connect user id

     Requires authentication as user

    Args:
        connect_user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConnectConnectAuthenticationExchangeResult]
    """

    return (
        await asyncio_detailed(
            client=client,
            connect_user_id=connect_user_id,
        )
    ).parsed
