from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.media_info_playback_info_request import MediaInfoPlaybackInfoRequest
from ...models.media_info_playback_info_response import MediaInfoPlaybackInfoResponse
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: MediaInfoPlaybackInfoRequest,
) -> Dict[str, Any]:
    url = "{}/Items/{Id}/PlaybackInfo".format(client.base_url, Id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, MediaInfoPlaybackInfoResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = MediaInfoPlaybackInfoResponse.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, MediaInfoPlaybackInfoResponse]]:
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
    json_body: MediaInfoPlaybackInfoRequest,
) -> Response[Union[Any, MediaInfoPlaybackInfoResponse]]:
    """Gets live playback media info for an item

     Requires authentication as user

    Args:
        id (str):
        json_body (MediaInfoPlaybackInfoRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, MediaInfoPlaybackInfoResponse]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
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
    json_body: MediaInfoPlaybackInfoRequest,
) -> Optional[Union[Any, MediaInfoPlaybackInfoResponse]]:
    """Gets live playback media info for an item

     Requires authentication as user

    Args:
        id (str):
        json_body (MediaInfoPlaybackInfoRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, MediaInfoPlaybackInfoResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: MediaInfoPlaybackInfoRequest,
) -> Response[Union[Any, MediaInfoPlaybackInfoResponse]]:
    """Gets live playback media info for an item

     Requires authentication as user

    Args:
        id (str):
        json_body (MediaInfoPlaybackInfoRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, MediaInfoPlaybackInfoResponse]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: MediaInfoPlaybackInfoRequest,
) -> Optional[Union[Any, MediaInfoPlaybackInfoResponse]]:
    """Gets live playback media info for an item

     Requires authentication as user

    Args:
        id (str):
        json_body (MediaInfoPlaybackInfoRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, MediaInfoPlaybackInfoResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
