from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.query_result_emby_live_tv_channel_management_info import QueryResultEmbyLiveTVChannelManagementInfo
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort_by: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/LiveTv/Manage/Channels".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["StartIndex"] = start_index

    params["Limit"] = limit

    params["SortBy"] = sort_by

    params["SortOrder"] = sort_order

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
) -> Optional[Union[Any, QueryResultEmbyLiveTVChannelManagementInfo]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = QueryResultEmbyLiveTVChannelManagementInfo.from_dict(response.json())

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
) -> Response[Union[Any, QueryResultEmbyLiveTVChannelManagementInfo]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort_by: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, QueryResultEmbyLiveTVChannelManagementInfo]]:
    """Gets the channel management list

     Requires authentication as administrator

    Args:
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        sort_by (Union[Unset, None, str]):
        sort_order (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultEmbyLiveTVChannelManagementInfo]]
    """

    kwargs = _get_kwargs(
        client=client,
        start_index=start_index,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort_by: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, QueryResultEmbyLiveTVChannelManagementInfo]]:
    """Gets the channel management list

     Requires authentication as administrator

    Args:
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        sort_by (Union[Unset, None, str]):
        sort_order (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultEmbyLiveTVChannelManagementInfo]
    """

    return sync_detailed(
        client=client,
        start_index=start_index,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort_by: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, QueryResultEmbyLiveTVChannelManagementInfo]]:
    """Gets the channel management list

     Requires authentication as administrator

    Args:
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        sort_by (Union[Unset, None, str]):
        sort_order (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultEmbyLiveTVChannelManagementInfo]]
    """

    kwargs = _get_kwargs(
        client=client,
        start_index=start_index,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort_by: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, QueryResultEmbyLiveTVChannelManagementInfo]]:
    """Gets the channel management list

     Requires authentication as administrator

    Args:
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        sort_by (Union[Unset, None, str]):
        sort_order (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultEmbyLiveTVChannelManagementInfo]
    """

    return (
        await asyncio_detailed(
            client=client,
            start_index=start_index,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    ).parsed
