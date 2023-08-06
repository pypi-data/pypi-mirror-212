from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.query_result_activity_log_entry import QueryResultActivityLogEntry
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    min_date: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/System/ActivityLog/Entries".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["StartIndex"] = start_index

    params["Limit"] = limit

    params["MinDate"] = min_date

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, QueryResultActivityLogEntry]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = QueryResultActivityLogEntry.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, QueryResultActivityLogEntry]]:
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
    min_date: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, QueryResultActivityLogEntry]]:
    """Gets activity log entries

     Requires authentication as administrator

    Args:
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        min_date (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultActivityLogEntry]]
    """

    kwargs = _get_kwargs(
        client=client,
        start_index=start_index,
        limit=limit,
        min_date=min_date,
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
    min_date: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, QueryResultActivityLogEntry]]:
    """Gets activity log entries

     Requires authentication as administrator

    Args:
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        min_date (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultActivityLogEntry]
    """

    return sync_detailed(
        client=client,
        start_index=start_index,
        limit=limit,
        min_date=min_date,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    min_date: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, QueryResultActivityLogEntry]]:
    """Gets activity log entries

     Requires authentication as administrator

    Args:
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        min_date (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultActivityLogEntry]]
    """

    kwargs = _get_kwargs(
        client=client,
        start_index=start_index,
        limit=limit,
        min_date=min_date,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    min_date: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, QueryResultActivityLogEntry]]:
    """Gets activity log entries

     Requires authentication as administrator

    Args:
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        min_date (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultActivityLogEntry]
    """

    return (
        await asyncio_detailed(
            client=client,
            start_index=start_index,
            limit=limit,
            min_date=min_date,
        )
    ).parsed
