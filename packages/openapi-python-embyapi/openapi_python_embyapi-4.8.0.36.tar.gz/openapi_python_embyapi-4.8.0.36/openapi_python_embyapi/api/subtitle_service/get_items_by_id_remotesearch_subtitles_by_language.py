from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.remote_subtitle_info import RemoteSubtitleInfo
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    language: str,
    *,
    client: AuthenticatedClient,
    media_source_id: str,
    is_perfect_match: Union[Unset, None, bool] = UNSET,
    is_forced: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/Items/{Id}/RemoteSearch/Subtitles/{Language}".format(client.base_url, Id=id, Language=language)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["MediaSourceId"] = media_source_id

    params["IsPerfectMatch"] = is_perfect_match

    params["IsForced"] = is_forced

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, List["RemoteSubtitleInfo"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RemoteSubtitleInfo.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, List["RemoteSubtitleInfo"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    language: str,
    *,
    client: AuthenticatedClient,
    media_source_id: str,
    is_perfect_match: Union[Unset, None, bool] = UNSET,
    is_forced: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, List["RemoteSubtitleInfo"]]]:
    """Requires authentication as user

    Args:
        id (str):
        language (str):
        media_source_id (str):
        is_perfect_match (Union[Unset, None, bool]):
        is_forced (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['RemoteSubtitleInfo']]]
    """

    kwargs = _get_kwargs(
        id=id,
        language=language,
        client=client,
        media_source_id=media_source_id,
        is_perfect_match=is_perfect_match,
        is_forced=is_forced,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    language: str,
    *,
    client: AuthenticatedClient,
    media_source_id: str,
    is_perfect_match: Union[Unset, None, bool] = UNSET,
    is_forced: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, List["RemoteSubtitleInfo"]]]:
    """Requires authentication as user

    Args:
        id (str):
        language (str):
        media_source_id (str):
        is_perfect_match (Union[Unset, None, bool]):
        is_forced (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['RemoteSubtitleInfo']]
    """

    return sync_detailed(
        id=id,
        language=language,
        client=client,
        media_source_id=media_source_id,
        is_perfect_match=is_perfect_match,
        is_forced=is_forced,
    ).parsed


async def asyncio_detailed(
    id: str,
    language: str,
    *,
    client: AuthenticatedClient,
    media_source_id: str,
    is_perfect_match: Union[Unset, None, bool] = UNSET,
    is_forced: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, List["RemoteSubtitleInfo"]]]:
    """Requires authentication as user

    Args:
        id (str):
        language (str):
        media_source_id (str):
        is_perfect_match (Union[Unset, None, bool]):
        is_forced (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['RemoteSubtitleInfo']]]
    """

    kwargs = _get_kwargs(
        id=id,
        language=language,
        client=client,
        media_source_id=media_source_id,
        is_perfect_match=is_perfect_match,
        is_forced=is_forced,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    language: str,
    *,
    client: AuthenticatedClient,
    media_source_id: str,
    is_perfect_match: Union[Unset, None, bool] = UNSET,
    is_forced: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, List["RemoteSubtitleInfo"]]]:
    """Requires authentication as user

    Args:
        id (str):
        language (str):
        media_source_id (str):
        is_perfect_match (Union[Unset, None, bool]):
        is_forced (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['RemoteSubtitleInfo']]
    """

    return (
        await asyncio_detailed(
            id=id,
            language=language,
            client=client,
            media_source_id=media_source_id,
            is_perfect_match=is_perfect_match,
            is_forced=is_forced,
        )
    ).parsed
