from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.live_tv_listings_provider_info import LiveTvListingsProviderInfo
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    channel_id: str,
) -> Dict[str, Any]:
    url = "{}/LiveTv/ListingProviders".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ChannelId"] = channel_id

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


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[Any, List["LiveTvListingsProviderInfo"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = LiveTvListingsProviderInfo.from_dict(response_200_item_data)

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


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, List["LiveTvListingsProviderInfo"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    channel_id: str,
) -> Response[Union[Any, List["LiveTvListingsProviderInfo"]]]:
    """Gets current listing providers

     Requires authentication as administrator

    Args:
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['LiveTvListingsProviderInfo']]]
    """

    kwargs = _get_kwargs(
        client=client,
        channel_id=channel_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    channel_id: str,
) -> Optional[Union[Any, List["LiveTvListingsProviderInfo"]]]:
    """Gets current listing providers

     Requires authentication as administrator

    Args:
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['LiveTvListingsProviderInfo']]
    """

    return sync_detailed(
        client=client,
        channel_id=channel_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    channel_id: str,
) -> Response[Union[Any, List["LiveTvListingsProviderInfo"]]]:
    """Gets current listing providers

     Requires authentication as administrator

    Args:
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['LiveTvListingsProviderInfo']]]
    """

    kwargs = _get_kwargs(
        client=client,
        channel_id=channel_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    channel_id: str,
) -> Optional[Union[Any, List["LiveTvListingsProviderInfo"]]]:
    """Gets current listing providers

     Requires authentication as administrator

    Args:
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['LiveTvListingsProviderInfo']]
    """

    return (
        await asyncio_detailed(
            client=client,
            channel_id=channel_id,
        )
    ).parsed
