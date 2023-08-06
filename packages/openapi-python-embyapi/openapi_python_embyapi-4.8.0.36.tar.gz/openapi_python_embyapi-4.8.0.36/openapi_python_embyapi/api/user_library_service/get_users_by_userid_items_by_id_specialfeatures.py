from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.base_item_dto import BaseItemDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_id: str,
    id: str,
    *,
    client: AuthenticatedClient,
    fields: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/Users/{UserId}/Items/{Id}/SpecialFeatures".format(client.base_url, UserId=user_id, Id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["Fields"] = fields

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, List["BaseItemDto"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = BaseItemDto.from_dict(response_200_item_data)

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, List["BaseItemDto"]]]:
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
    fields: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, List["BaseItemDto"]]]:
    """Gets special features for an item

     Requires authentication as user

    Args:
        user_id (str):
        id (str):
        fields (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        enable_user_data (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['BaseItemDto']]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        id=id,
        client=client,
        fields=fields,
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
    user_id: str,
    id: str,
    *,
    client: AuthenticatedClient,
    fields: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, List["BaseItemDto"]]]:
    """Gets special features for an item

     Requires authentication as user

    Args:
        user_id (str):
        id (str):
        fields (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        enable_user_data (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['BaseItemDto']]
    """

    return sync_detailed(
        user_id=user_id,
        id=id,
        client=client,
        fields=fields,
        enable_images=enable_images,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
        enable_user_data=enable_user_data,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    id: str,
    *,
    client: AuthenticatedClient,
    fields: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, List["BaseItemDto"]]]:
    """Gets special features for an item

     Requires authentication as user

    Args:
        user_id (str):
        id (str):
        fields (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        enable_user_data (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['BaseItemDto']]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        id=id,
        client=client,
        fields=fields,
        enable_images=enable_images,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
        enable_user_data=enable_user_data,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    id: str,
    *,
    client: AuthenticatedClient,
    fields: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, List["BaseItemDto"]]]:
    """Gets special features for an item

     Requires authentication as user

    Args:
        user_id (str):
        id (str):
        fields (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        enable_user_data (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['BaseItemDto']]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            id=id,
            client=client,
            fields=fields,
            enable_images=enable_images,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            enable_user_data=enable_user_data,
        )
    ).parsed
