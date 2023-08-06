from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.display_preferences import DisplayPreferences
from ...types import UNSET, Response


def _get_kwargs(
    display_preferences_id: str,
    *,
    client: AuthenticatedClient,
    json_body: DisplayPreferences,
    user_id: str,
) -> Dict[str, Any]:
    url = "{}/DisplayPreferences/{DisplayPreferencesId}".format(
        client.base_url, DisplayPreferencesId=display_preferences_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["UserId"] = user_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
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
    display_preferences_id: str,
    *,
    client: AuthenticatedClient,
    json_body: DisplayPreferences,
    user_id: str,
) -> Response[Any]:
    """Updates a user's display preferences for an item

     Requires authentication as user

    Args:
        display_preferences_id (str):
        user_id (str):
        json_body (DisplayPreferences):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        display_preferences_id=display_preferences_id,
        client=client,
        json_body=json_body,
        user_id=user_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    display_preferences_id: str,
    *,
    client: AuthenticatedClient,
    json_body: DisplayPreferences,
    user_id: str,
) -> Response[Any]:
    """Updates a user's display preferences for an item

     Requires authentication as user

    Args:
        display_preferences_id (str):
        user_id (str):
        json_body (DisplayPreferences):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        display_preferences_id=display_preferences_id,
        client=client,
        json_body=json_body,
        user_id=user_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
