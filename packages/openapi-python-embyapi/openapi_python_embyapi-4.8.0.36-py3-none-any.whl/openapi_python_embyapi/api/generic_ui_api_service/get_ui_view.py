from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.emby_web_generic_ui_model_ui_view_info import EmbyWebGenericUIModelUIViewInfo
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    page_id: str,
    client_locale: str,
) -> Dict[str, Any]:
    url = "{}/UI/View".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["PageId"] = page_id

    params["ClientLocale"] = client_locale

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
) -> Optional[Union[Any, EmbyWebGenericUIModelUIViewInfo]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = EmbyWebGenericUIModelUIViewInfo.from_dict(response.json())

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
) -> Response[Union[Any, EmbyWebGenericUIModelUIViewInfo]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page_id: str,
    client_locale: str,
) -> Response[Union[Any, EmbyWebGenericUIModelUIViewInfo]]:
    """Gets UI view data

     Requires authentication as user

    Args:
        page_id (str):
        client_locale (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, EmbyWebGenericUIModelUIViewInfo]]
    """

    kwargs = _get_kwargs(
        client=client,
        page_id=page_id,
        client_locale=client_locale,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    page_id: str,
    client_locale: str,
) -> Optional[Union[Any, EmbyWebGenericUIModelUIViewInfo]]:
    """Gets UI view data

     Requires authentication as user

    Args:
        page_id (str):
        client_locale (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, EmbyWebGenericUIModelUIViewInfo]
    """

    return sync_detailed(
        client=client,
        page_id=page_id,
        client_locale=client_locale,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page_id: str,
    client_locale: str,
) -> Response[Union[Any, EmbyWebGenericUIModelUIViewInfo]]:
    """Gets UI view data

     Requires authentication as user

    Args:
        page_id (str):
        client_locale (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, EmbyWebGenericUIModelUIViewInfo]]
    """

    kwargs = _get_kwargs(
        client=client,
        page_id=page_id,
        client_locale=client_locale,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    page_id: str,
    client_locale: str,
) -> Optional[Union[Any, EmbyWebGenericUIModelUIViewInfo]]:
    """Gets UI view data

     Requires authentication as user

    Args:
        page_id (str):
        client_locale (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, EmbyWebGenericUIModelUIViewInfo]
    """

    return (
        await asyncio_detailed(
            client=client,
            page_id=page_id,
            client_locale=client_locale,
        )
    ).parsed
