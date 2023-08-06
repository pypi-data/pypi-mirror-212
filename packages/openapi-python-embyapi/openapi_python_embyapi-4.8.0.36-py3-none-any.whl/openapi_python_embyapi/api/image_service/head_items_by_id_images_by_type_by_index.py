from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.image_type import ImageType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    type: ImageType,
    index: int,
    *,
    client: Client,
    max_width: Union[Unset, None, int] = UNSET,
    max_height: Union[Unset, None, int] = UNSET,
    width: Union[Unset, None, int] = UNSET,
    height: Union[Unset, None, int] = UNSET,
    quality: Union[Unset, None, int] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    crop_whitespace: Union[Unset, None, bool] = UNSET,
    enable_image_enhancers: Union[Unset, None, bool] = UNSET,
    format_: Union[Unset, None, str] = UNSET,
    background_color: Union[Unset, None, str] = UNSET,
    foreground_layer: Union[Unset, None, str] = UNSET,
    auto_orient: Union[Unset, None, bool] = UNSET,
    keep_animation: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/Items/{Id}/Images/{Type}/{Index}".format(client.base_url, Id=id, Type=type, Index=index)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["MaxWidth"] = max_width

    params["MaxHeight"] = max_height

    params["Width"] = width

    params["Height"] = height

    params["Quality"] = quality

    params["Tag"] = tag

    params["CropWhitespace"] = crop_whitespace

    params["EnableImageEnhancers"] = enable_image_enhancers

    params["Format"] = format_

    params["BackgroundColor"] = background_color

    params["ForegroundLayer"] = foreground_layer

    params["AutoOrient"] = auto_orient

    params["KeepAnimation"] = keep_animation

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "head",
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
    id: str,
    type: ImageType,
    index: int,
    *,
    client: Client,
    max_width: Union[Unset, None, int] = UNSET,
    max_height: Union[Unset, None, int] = UNSET,
    width: Union[Unset, None, int] = UNSET,
    height: Union[Unset, None, int] = UNSET,
    quality: Union[Unset, None, int] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    crop_whitespace: Union[Unset, None, bool] = UNSET,
    enable_image_enhancers: Union[Unset, None, bool] = UNSET,
    format_: Union[Unset, None, str] = UNSET,
    background_color: Union[Unset, None, str] = UNSET,
    foreground_layer: Union[Unset, None, str] = UNSET,
    auto_orient: Union[Unset, None, bool] = UNSET,
    keep_animation: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """No authentication required

    Args:
        id (str):
        type (ImageType):
        index (int):
        max_width (Union[Unset, None, int]):
        max_height (Union[Unset, None, int]):
        width (Union[Unset, None, int]):
        height (Union[Unset, None, int]):
        quality (Union[Unset, None, int]):
        tag (Union[Unset, None, str]):
        crop_whitespace (Union[Unset, None, bool]):
        enable_image_enhancers (Union[Unset, None, bool]):
        format_ (Union[Unset, None, str]):
        background_color (Union[Unset, None, str]):
        foreground_layer (Union[Unset, None, str]):
        auto_orient (Union[Unset, None, bool]):
        keep_animation (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        type=type,
        index=index,
        client=client,
        max_width=max_width,
        max_height=max_height,
        width=width,
        height=height,
        quality=quality,
        tag=tag,
        crop_whitespace=crop_whitespace,
        enable_image_enhancers=enable_image_enhancers,
        format_=format_,
        background_color=background_color,
        foreground_layer=foreground_layer,
        auto_orient=auto_orient,
        keep_animation=keep_animation,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    id: str,
    type: ImageType,
    index: int,
    *,
    client: Client,
    max_width: Union[Unset, None, int] = UNSET,
    max_height: Union[Unset, None, int] = UNSET,
    width: Union[Unset, None, int] = UNSET,
    height: Union[Unset, None, int] = UNSET,
    quality: Union[Unset, None, int] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    crop_whitespace: Union[Unset, None, bool] = UNSET,
    enable_image_enhancers: Union[Unset, None, bool] = UNSET,
    format_: Union[Unset, None, str] = UNSET,
    background_color: Union[Unset, None, str] = UNSET,
    foreground_layer: Union[Unset, None, str] = UNSET,
    auto_orient: Union[Unset, None, bool] = UNSET,
    keep_animation: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """No authentication required

    Args:
        id (str):
        type (ImageType):
        index (int):
        max_width (Union[Unset, None, int]):
        max_height (Union[Unset, None, int]):
        width (Union[Unset, None, int]):
        height (Union[Unset, None, int]):
        quality (Union[Unset, None, int]):
        tag (Union[Unset, None, str]):
        crop_whitespace (Union[Unset, None, bool]):
        enable_image_enhancers (Union[Unset, None, bool]):
        format_ (Union[Unset, None, str]):
        background_color (Union[Unset, None, str]):
        foreground_layer (Union[Unset, None, str]):
        auto_orient (Union[Unset, None, bool]):
        keep_animation (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        type=type,
        index=index,
        client=client,
        max_width=max_width,
        max_height=max_height,
        width=width,
        height=height,
        quality=quality,
        tag=tag,
        crop_whitespace=crop_whitespace,
        enable_image_enhancers=enable_image_enhancers,
        format_=format_,
        background_color=background_color,
        foreground_layer=foreground_layer,
        auto_orient=auto_orient,
        keep_animation=keep_animation,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
