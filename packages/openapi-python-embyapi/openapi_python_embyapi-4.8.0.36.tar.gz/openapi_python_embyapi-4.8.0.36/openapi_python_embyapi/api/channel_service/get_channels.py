from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.query_result_base_item_dto import QueryResultBaseItemDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    user_id: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/Channels".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["UserId"] = user_id

    params["StartIndex"] = start_index

    params["Fields"] = fields

    params["Limit"] = limit

    params["EnableImages"] = enable_images

    params["ImageTypeLimit"] = image_type_limit

    params["EnableImageTypes"] = enable_image_types

    params["EnableUserData"] = enable_user_data

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, QueryResultBaseItemDto]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = QueryResultBaseItemDto.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, QueryResultBaseItemDto]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    user_id: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, QueryResultBaseItemDto]]:
    """Gets available channels

     Requires authentication as user

    Args:
        user_id (Union[Unset, None, str]):
        start_index (Union[Unset, None, int]):
        fields (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        enable_images (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        enable_user_data (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultBaseItemDto]]
    """

    kwargs = _get_kwargs(
        client=client,
        user_id=user_id,
        start_index=start_index,
        fields=fields,
        limit=limit,
        enable_images=enable_images,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
        enable_user_data=enable_user_data,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    user_id: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, QueryResultBaseItemDto]]:
    """Gets available channels

     Requires authentication as user

    Args:
        user_id (Union[Unset, None, str]):
        start_index (Union[Unset, None, int]):
        fields (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        enable_images (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        enable_user_data (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultBaseItemDto]
    """

    return sync_detailed(
        client=client,
        user_id=user_id,
        start_index=start_index,
        fields=fields,
        limit=limit,
        enable_images=enable_images,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
        enable_user_data=enable_user_data,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    user_id: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, QueryResultBaseItemDto]]:
    """Gets available channels

     Requires authentication as user

    Args:
        user_id (Union[Unset, None, str]):
        start_index (Union[Unset, None, int]):
        fields (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        enable_images (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        enable_user_data (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultBaseItemDto]]
    """

    kwargs = _get_kwargs(
        client=client,
        user_id=user_id,
        start_index=start_index,
        fields=fields,
        limit=limit,
        enable_images=enable_images,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
        enable_user_data=enable_user_data,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    user_id: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, QueryResultBaseItemDto]]:
    """Gets available channels

     Requires authentication as user

    Args:
        user_id (Union[Unset, None, str]):
        start_index (Union[Unset, None, int]):
        fields (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        enable_images (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        enable_user_data (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultBaseItemDto]
    """

    return (
        await asyncio_detailed(
            client=client,
            user_id=user_id,
            start_index=start_index,
            fields=fields,
            limit=limit,
            enable_images=enable_images,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            enable_user_data=enable_user_data,
        )
    ).parsed
