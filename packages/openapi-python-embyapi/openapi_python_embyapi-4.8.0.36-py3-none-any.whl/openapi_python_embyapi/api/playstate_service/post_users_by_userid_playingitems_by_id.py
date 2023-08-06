from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.play_method import PlayMethod
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_id: str,
    id: str,
    *,
    client: AuthenticatedClient,
    media_source_id: str,
    can_seek: Union[Unset, None, bool] = UNSET,
    audio_stream_index: Union[Unset, None, int] = UNSET,
    subtitle_stream_index: Union[Unset, None, int] = UNSET,
    play_method: Union[Unset, None, PlayMethod] = UNSET,
    live_stream_id: Union[Unset, None, str] = UNSET,
    play_session_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/Users/{UserId}/PlayingItems/{Id}".format(client.base_url, UserId=user_id, Id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["MediaSourceId"] = media_source_id

    params["CanSeek"] = can_seek

    params["AudioStreamIndex"] = audio_stream_index

    params["SubtitleStreamIndex"] = subtitle_stream_index

    json_play_method: Union[Unset, None, str] = UNSET
    if not isinstance(play_method, Unset):
        json_play_method = play_method.value if play_method else None

    params["PlayMethod"] = json_play_method

    params["LiveStreamId"] = live_stream_id

    params["PlaySessionId"] = play_session_id

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
    user_id: str,
    id: str,
    *,
    client: AuthenticatedClient,
    media_source_id: str,
    can_seek: Union[Unset, None, bool] = UNSET,
    audio_stream_index: Union[Unset, None, int] = UNSET,
    subtitle_stream_index: Union[Unset, None, int] = UNSET,
    play_method: Union[Unset, None, PlayMethod] = UNSET,
    live_stream_id: Union[Unset, None, str] = UNSET,
    play_session_id: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Reports that a user has begun playing an item

     Requires authentication as user

    Args:
        user_id (str):
        id (str):
        media_source_id (str):
        can_seek (Union[Unset, None, bool]):
        audio_stream_index (Union[Unset, None, int]):
        subtitle_stream_index (Union[Unset, None, int]):
        play_method (Union[Unset, None, PlayMethod]):
        live_stream_id (Union[Unset, None, str]):
        play_session_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        id=id,
        client=client,
        media_source_id=media_source_id,
        can_seek=can_seek,
        audio_stream_index=audio_stream_index,
        subtitle_stream_index=subtitle_stream_index,
        play_method=play_method,
        live_stream_id=live_stream_id,
        play_session_id=play_session_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    user_id: str,
    id: str,
    *,
    client: AuthenticatedClient,
    media_source_id: str,
    can_seek: Union[Unset, None, bool] = UNSET,
    audio_stream_index: Union[Unset, None, int] = UNSET,
    subtitle_stream_index: Union[Unset, None, int] = UNSET,
    play_method: Union[Unset, None, PlayMethod] = UNSET,
    live_stream_id: Union[Unset, None, str] = UNSET,
    play_session_id: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Reports that a user has begun playing an item

     Requires authentication as user

    Args:
        user_id (str):
        id (str):
        media_source_id (str):
        can_seek (Union[Unset, None, bool]):
        audio_stream_index (Union[Unset, None, int]):
        subtitle_stream_index (Union[Unset, None, int]):
        play_method (Union[Unset, None, PlayMethod]):
        live_stream_id (Union[Unset, None, str]):
        play_session_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        id=id,
        client=client,
        media_source_id=media_source_id,
        can_seek=can_seek,
        audio_stream_index=audio_stream_index,
        subtitle_stream_index=subtitle_stream_index,
        play_method=play_method,
        live_stream_id=live_stream_id,
        play_session_id=play_session_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
