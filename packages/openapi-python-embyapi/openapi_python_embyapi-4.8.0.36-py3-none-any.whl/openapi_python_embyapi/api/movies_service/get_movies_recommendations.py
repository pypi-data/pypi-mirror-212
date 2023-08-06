from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.recommendation_dto import RecommendationDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    category_limit: Union[Unset, None, int] = UNSET,
    item_limit: Union[Unset, None, int] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/Movies/Recommendations".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["CategoryLimit"] = category_limit

    params["ItemLimit"] = item_limit

    params["UserId"] = user_id

    params["ParentId"] = parent_id

    params["EnableImages"] = enable_images

    params["EnableUserData"] = enable_user_data

    params["ImageTypeLimit"] = image_type_limit

    params["EnableImageTypes"] = enable_image_types

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, List["RecommendationDto"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RecommendationDto.from_dict(response_200_item_data)

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, List["RecommendationDto"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    category_limit: Union[Unset, None, int] = UNSET,
    item_limit: Union[Unset, None, int] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, List["RecommendationDto"]]]:
    """Gets movie recommendations

     Requires authentication as user

    Args:
        category_limit (Union[Unset, None, int]):
        item_limit (Union[Unset, None, int]):
        user_id (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['RecommendationDto']]]
    """

    kwargs = _get_kwargs(
        client=client,
        category_limit=category_limit,
        item_limit=item_limit,
        user_id=user_id,
        parent_id=parent_id,
        enable_images=enable_images,
        enable_user_data=enable_user_data,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    category_limit: Union[Unset, None, int] = UNSET,
    item_limit: Union[Unset, None, int] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, List["RecommendationDto"]]]:
    """Gets movie recommendations

     Requires authentication as user

    Args:
        category_limit (Union[Unset, None, int]):
        item_limit (Union[Unset, None, int]):
        user_id (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['RecommendationDto']]
    """

    return sync_detailed(
        client=client,
        category_limit=category_limit,
        item_limit=item_limit,
        user_id=user_id,
        parent_id=parent_id,
        enable_images=enable_images,
        enable_user_data=enable_user_data,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    category_limit: Union[Unset, None, int] = UNSET,
    item_limit: Union[Unset, None, int] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, List["RecommendationDto"]]]:
    """Gets movie recommendations

     Requires authentication as user

    Args:
        category_limit (Union[Unset, None, int]):
        item_limit (Union[Unset, None, int]):
        user_id (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['RecommendationDto']]]
    """

    kwargs = _get_kwargs(
        client=client,
        category_limit=category_limit,
        item_limit=item_limit,
        user_id=user_id,
        parent_id=parent_id,
        enable_images=enable_images,
        enable_user_data=enable_user_data,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    category_limit: Union[Unset, None, int] = UNSET,
    item_limit: Union[Unset, None, int] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, List["RecommendationDto"]]]:
    """Gets movie recommendations

     Requires authentication as user

    Args:
        category_limit (Union[Unset, None, int]):
        item_limit (Union[Unset, None, int]):
        user_id (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['RecommendationDto']]
    """

    return (
        await asyncio_detailed(
            client=client,
            category_limit=category_limit,
            item_limit=item_limit,
            user_id=user_id,
            parent_id=parent_id,
            enable_images=enable_images,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
        )
    ).parsed
