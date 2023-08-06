from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.query_result_base_item_dto import QueryResultBaseItemDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: AuthenticatedClient,
    include_item_types: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/Albums/{Id}/InstantMix".format(client.base_url, Id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["IncludeItemTypes"] = include_item_types

    params["EnableImages"] = enable_images

    params["EnableUserData"] = enable_user_data

    params["ImageTypeLimit"] = image_type_limit

    params["EnableImageTypes"] = enable_image_types

    params["UserId"] = user_id

    params["Limit"] = limit

    params["Fields"] = fields

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
    id: str,
    *,
    client: AuthenticatedClient,
    include_item_types: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, QueryResultBaseItemDto]]:
    """Creates an instant playlist based on a given album

     Requires authentication as user

    Args:
        id (str):
        include_item_types (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        user_id (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        fields (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultBaseItemDto]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        include_item_types=include_item_types,
        enable_images=enable_images,
        enable_user_data=enable_user_data,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
        user_id=user_id,
        limit=limit,
        fields=fields,
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
    include_item_types: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, QueryResultBaseItemDto]]:
    """Creates an instant playlist based on a given album

     Requires authentication as user

    Args:
        id (str):
        include_item_types (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        user_id (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        fields (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultBaseItemDto]
    """

    return sync_detailed(
        id=id,
        client=client,
        include_item_types=include_item_types,
        enable_images=enable_images,
        enable_user_data=enable_user_data,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
        user_id=user_id,
        limit=limit,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    include_item_types: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, QueryResultBaseItemDto]]:
    """Creates an instant playlist based on a given album

     Requires authentication as user

    Args:
        id (str):
        include_item_types (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        user_id (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        fields (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultBaseItemDto]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        include_item_types=include_item_types,
        enable_images=enable_images,
        enable_user_data=enable_user_data,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
        user_id=user_id,
        limit=limit,
        fields=fields,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    include_item_types: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, QueryResultBaseItemDto]]:
    """Creates an instant playlist based on a given album

     Requires authentication as user

    Args:
        id (str):
        include_item_types (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        user_id (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        fields (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultBaseItemDto]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            include_item_types=include_item_types,
            enable_images=enable_images,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            user_id=user_id,
            limit=limit,
            fields=fields,
        )
    ).parsed
