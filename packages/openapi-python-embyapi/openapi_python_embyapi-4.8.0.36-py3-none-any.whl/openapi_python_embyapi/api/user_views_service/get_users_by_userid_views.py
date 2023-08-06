from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.query_result_base_item_dto import QueryResultBaseItemDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_id: str,
    *,
    client: Client,
    include_external_content: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/Users/{UserId}/Views".format(client.base_url, UserId=user_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["IncludeExternalContent"] = include_external_content

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
    user_id: str,
    *,
    client: Client,
    include_external_content: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, QueryResultBaseItemDto]]:
    """No authentication required

    Args:
        user_id (str):
        include_external_content (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultBaseItemDto]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        client=client,
        include_external_content=include_external_content,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: Client,
    include_external_content: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, QueryResultBaseItemDto]]:
    """No authentication required

    Args:
        user_id (str):
        include_external_content (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultBaseItemDto]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        include_external_content=include_external_content,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: Client,
    include_external_content: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, QueryResultBaseItemDto]]:
    """No authentication required

    Args:
        user_id (str):
        include_external_content (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultBaseItemDto]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        client=client,
        include_external_content=include_external_content,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: Client,
    include_external_content: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, QueryResultBaseItemDto]]:
    """No authentication required

    Args:
        user_id (str):
        include_external_content (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultBaseItemDto]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            include_external_content=include_external_content,
        )
    ).parsed
