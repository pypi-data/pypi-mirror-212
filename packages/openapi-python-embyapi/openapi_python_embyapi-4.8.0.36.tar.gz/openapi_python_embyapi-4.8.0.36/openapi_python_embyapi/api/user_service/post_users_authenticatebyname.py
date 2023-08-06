from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.authenticate_user_by_name import AuthenticateUserByName
from ...models.authentication_authentication_result import AuthenticationAuthenticationResult
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: AuthenticateUserByName,
    x_emby_authorization: str,
) -> Dict[str, Any]:
    url = "{}/Users/AuthenticateByName".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    headers["X-Emby-Authorization"] = x_emby_authorization

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[Any, AuthenticationAuthenticationResult]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AuthenticationAuthenticationResult.from_dict(response.json())

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
) -> Response[Union[Any, AuthenticationAuthenticationResult]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: AuthenticateUserByName,
    x_emby_authorization: str,
) -> Response[Union[Any, AuthenticationAuthenticationResult]]:
    """Authenticates a user

     Authenticate a user by nane and password. A 200 status code indicates success, while anything in the
    400 or 500 range indicates failure
    ---
    No authentication required

    Args:
        x_emby_authorization (str):
        json_body (AuthenticateUserByName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, AuthenticationAuthenticationResult]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        x_emby_authorization=x_emby_authorization,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    json_body: AuthenticateUserByName,
    x_emby_authorization: str,
) -> Optional[Union[Any, AuthenticationAuthenticationResult]]:
    """Authenticates a user

     Authenticate a user by nane and password. A 200 status code indicates success, while anything in the
    400 or 500 range indicates failure
    ---
    No authentication required

    Args:
        x_emby_authorization (str):
        json_body (AuthenticateUserByName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, AuthenticationAuthenticationResult]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        x_emby_authorization=x_emby_authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: AuthenticateUserByName,
    x_emby_authorization: str,
) -> Response[Union[Any, AuthenticationAuthenticationResult]]:
    """Authenticates a user

     Authenticate a user by nane and password. A 200 status code indicates success, while anything in the
    400 or 500 range indicates failure
    ---
    No authentication required

    Args:
        x_emby_authorization (str):
        json_body (AuthenticateUserByName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, AuthenticationAuthenticationResult]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        x_emby_authorization=x_emby_authorization,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: AuthenticateUserByName,
    x_emby_authorization: str,
) -> Optional[Union[Any, AuthenticationAuthenticationResult]]:
    """Authenticates a user

     Authenticate a user by nane and password. A 200 status code indicates success, while anything in the
    400 or 500 range indicates failure
    ---
    No authentication required

    Args:
        x_emby_authorization (str):
        json_body (AuthenticateUserByName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, AuthenticationAuthenticationResult]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            x_emby_authorization=x_emby_authorization,
        )
    ).parsed
