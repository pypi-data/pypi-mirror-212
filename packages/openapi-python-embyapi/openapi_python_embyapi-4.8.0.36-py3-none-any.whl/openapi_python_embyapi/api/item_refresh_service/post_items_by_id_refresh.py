from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.providers_metadata_refresh_mode import ProvidersMetadataRefreshMode
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: AuthenticatedClient,
    recursive: Union[Unset, None, bool] = UNSET,
    metadata_refresh_mode: Union[Unset, None, ProvidersMetadataRefreshMode] = UNSET,
    image_refresh_mode: Union[Unset, None, ProvidersMetadataRefreshMode] = UNSET,
    replace_all_metadata: Union[Unset, None, bool] = UNSET,
    replace_all_images: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/Items/{Id}/Refresh".format(client.base_url, Id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["Recursive"] = recursive

    json_metadata_refresh_mode: Union[Unset, None, str] = UNSET
    if not isinstance(metadata_refresh_mode, Unset):
        json_metadata_refresh_mode = metadata_refresh_mode.value if metadata_refresh_mode else None

    params["MetadataRefreshMode"] = json_metadata_refresh_mode

    json_image_refresh_mode: Union[Unset, None, str] = UNSET
    if not isinstance(image_refresh_mode, Unset):
        json_image_refresh_mode = image_refresh_mode.value if image_refresh_mode else None

    params["ImageRefreshMode"] = json_image_refresh_mode

    params["ReplaceAllMetadata"] = replace_all_metadata

    params["ReplaceAllImages"] = replace_all_images

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
    id: str,
    *,
    client: AuthenticatedClient,
    recursive: Union[Unset, None, bool] = UNSET,
    metadata_refresh_mode: Union[Unset, None, ProvidersMetadataRefreshMode] = UNSET,
    image_refresh_mode: Union[Unset, None, ProvidersMetadataRefreshMode] = UNSET,
    replace_all_metadata: Union[Unset, None, bool] = UNSET,
    replace_all_images: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Refreshes metadata for an item

     Requires authentication as user

    Args:
        id (str):
        recursive (Union[Unset, None, bool]):
        metadata_refresh_mode (Union[Unset, None, ProvidersMetadataRefreshMode]):
        image_refresh_mode (Union[Unset, None, ProvidersMetadataRefreshMode]):
        replace_all_metadata (Union[Unset, None, bool]):
        replace_all_images (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        recursive=recursive,
        metadata_refresh_mode=metadata_refresh_mode,
        image_refresh_mode=image_refresh_mode,
        replace_all_metadata=replace_all_metadata,
        replace_all_images=replace_all_images,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    recursive: Union[Unset, None, bool] = UNSET,
    metadata_refresh_mode: Union[Unset, None, ProvidersMetadataRefreshMode] = UNSET,
    image_refresh_mode: Union[Unset, None, ProvidersMetadataRefreshMode] = UNSET,
    replace_all_metadata: Union[Unset, None, bool] = UNSET,
    replace_all_images: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Refreshes metadata for an item

     Requires authentication as user

    Args:
        id (str):
        recursive (Union[Unset, None, bool]):
        metadata_refresh_mode (Union[Unset, None, ProvidersMetadataRefreshMode]):
        image_refresh_mode (Union[Unset, None, ProvidersMetadataRefreshMode]):
        replace_all_metadata (Union[Unset, None, bool]):
        replace_all_images (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        recursive=recursive,
        metadata_refresh_mode=metadata_refresh_mode,
        image_refresh_mode=image_refresh_mode,
        replace_all_metadata=replace_all_metadata,
        replace_all_images=replace_all_images,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
