from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.query_result_live_tv_series_timer_info_dto import QueryResultLiveTvSeriesTimerInfoDto
from ...models.sort_order import SortOrder
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    sort_by: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, SortOrder] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/LiveTv/SeriesTimers".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["SortBy"] = sort_by

    json_sort_order: Union[Unset, None, str] = UNSET
    if not isinstance(sort_order, Unset):
        json_sort_order = sort_order.value if sort_order else None

    params["SortOrder"] = json_sort_order

    params["StartIndex"] = start_index

    params["Limit"] = limit

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
) -> Optional[Union[Any, QueryResultLiveTvSeriesTimerInfoDto]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = QueryResultLiveTvSeriesTimerInfoDto.from_dict(response.json())

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
) -> Response[Union[Any, QueryResultLiveTvSeriesTimerInfoDto]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    sort_by: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, SortOrder] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Response[Union[Any, QueryResultLiveTvSeriesTimerInfoDto]]:
    """Gets live tv series timers

     Requires authentication as user

    Args:
        sort_by (Union[Unset, None, str]):
        sort_order (Union[Unset, None, SortOrder]):
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultLiveTvSeriesTimerInfoDto]]
    """

    kwargs = _get_kwargs(
        client=client,
        sort_by=sort_by,
        sort_order=sort_order,
        start_index=start_index,
        limit=limit,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    sort_by: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, SortOrder] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Optional[Union[Any, QueryResultLiveTvSeriesTimerInfoDto]]:
    """Gets live tv series timers

     Requires authentication as user

    Args:
        sort_by (Union[Unset, None, str]):
        sort_order (Union[Unset, None, SortOrder]):
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultLiveTvSeriesTimerInfoDto]
    """

    return sync_detailed(
        client=client,
        sort_by=sort_by,
        sort_order=sort_order,
        start_index=start_index,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    sort_by: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, SortOrder] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Response[Union[Any, QueryResultLiveTvSeriesTimerInfoDto]]:
    """Gets live tv series timers

     Requires authentication as user

    Args:
        sort_by (Union[Unset, None, str]):
        sort_order (Union[Unset, None, SortOrder]):
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultLiveTvSeriesTimerInfoDto]]
    """

    kwargs = _get_kwargs(
        client=client,
        sort_by=sort_by,
        sort_order=sort_order,
        start_index=start_index,
        limit=limit,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    sort_by: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, SortOrder] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Optional[Union[Any, QueryResultLiveTvSeriesTimerInfoDto]]:
    """Gets live tv series timers

     Requires authentication as user

    Args:
        sort_by (Union[Unset, None, str]):
        sort_order (Union[Unset, None, SortOrder]):
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultLiveTvSeriesTimerInfoDto]
    """

    return (
        await asyncio_detailed(
            client=client,
            sort_by=sort_by,
            sort_order=sort_order,
            start_index=start_index,
            limit=limit,
        )
    ).parsed
