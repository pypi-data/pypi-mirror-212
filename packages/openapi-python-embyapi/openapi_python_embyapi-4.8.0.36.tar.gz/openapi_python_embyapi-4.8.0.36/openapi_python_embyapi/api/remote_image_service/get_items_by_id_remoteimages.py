from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.image_type import ImageType
from ...models.remote_image_result import RemoteImageResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: AuthenticatedClient,
    type: Union[Unset, None, ImageType] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    provider_name: Union[Unset, None, str] = UNSET,
    include_all_languages: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/Items/{Id}/RemoteImages".format(client.base_url, Id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_type: Union[Unset, None, str] = UNSET
    if not isinstance(type, Unset):
        json_type = type.value if type else None

    params["Type"] = json_type

    params["StartIndex"] = start_index

    params["Limit"] = limit

    params["ProviderName"] = provider_name

    params["IncludeAllLanguages"] = include_all_languages

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, RemoteImageResult]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RemoteImageResult.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, RemoteImageResult]]:
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
    type: Union[Unset, None, ImageType] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    provider_name: Union[Unset, None, str] = UNSET,
    include_all_languages: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, RemoteImageResult]]:
    """Gets available remote images for an item

     Requires authentication as user

    Args:
        id (str):
        type (Union[Unset, None, ImageType]):
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        provider_name (Union[Unset, None, str]):
        include_all_languages (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, RemoteImageResult]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        type=type,
        start_index=start_index,
        limit=limit,
        provider_name=provider_name,
        include_all_languages=include_all_languages,
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
    type: Union[Unset, None, ImageType] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    provider_name: Union[Unset, None, str] = UNSET,
    include_all_languages: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, RemoteImageResult]]:
    """Gets available remote images for an item

     Requires authentication as user

    Args:
        id (str):
        type (Union[Unset, None, ImageType]):
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        provider_name (Union[Unset, None, str]):
        include_all_languages (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, RemoteImageResult]
    """

    return sync_detailed(
        id=id,
        client=client,
        type=type,
        start_index=start_index,
        limit=limit,
        provider_name=provider_name,
        include_all_languages=include_all_languages,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    type: Union[Unset, None, ImageType] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    provider_name: Union[Unset, None, str] = UNSET,
    include_all_languages: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, RemoteImageResult]]:
    """Gets available remote images for an item

     Requires authentication as user

    Args:
        id (str):
        type (Union[Unset, None, ImageType]):
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        provider_name (Union[Unset, None, str]):
        include_all_languages (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, RemoteImageResult]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        type=type,
        start_index=start_index,
        limit=limit,
        provider_name=provider_name,
        include_all_languages=include_all_languages,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    type: Union[Unset, None, ImageType] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    provider_name: Union[Unset, None, str] = UNSET,
    include_all_languages: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, RemoteImageResult]]:
    """Gets available remote images for an item

     Requires authentication as user

    Args:
        id (str):
        type (Union[Unset, None, ImageType]):
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        provider_name (Union[Unset, None, str]):
        include_all_languages (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, RemoteImageResult]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            type=type,
            start_index=start_index,
            limit=limit,
            provider_name=provider_name,
            include_all_languages=include_all_languages,
        )
    ).parsed
