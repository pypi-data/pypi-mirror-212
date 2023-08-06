from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.updates_package_info import UpdatesPackageInfo
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    package_type: Union[Unset, None, str] = UNSET,
    target_systems: Union[Unset, None, str] = UNSET,
    is_premium: Union[Unset, None, bool] = UNSET,
    is_adult: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/Packages".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["PackageType"] = package_type

    params["TargetSystems"] = target_systems

    params["IsPremium"] = is_premium

    params["IsAdult"] = is_adult

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, List["UpdatesPackageInfo"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UpdatesPackageInfo.from_dict(response_200_item_data)

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, List["UpdatesPackageInfo"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    package_type: Union[Unset, None, str] = UNSET,
    target_systems: Union[Unset, None, str] = UNSET,
    is_premium: Union[Unset, None, bool] = UNSET,
    is_adult: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, List["UpdatesPackageInfo"]]]:
    """Gets available packages

     Requires authentication as user

    Args:
        package_type (Union[Unset, None, str]):
        target_systems (Union[Unset, None, str]):
        is_premium (Union[Unset, None, bool]):
        is_adult (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['UpdatesPackageInfo']]]
    """

    kwargs = _get_kwargs(
        client=client,
        package_type=package_type,
        target_systems=target_systems,
        is_premium=is_premium,
        is_adult=is_adult,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    package_type: Union[Unset, None, str] = UNSET,
    target_systems: Union[Unset, None, str] = UNSET,
    is_premium: Union[Unset, None, bool] = UNSET,
    is_adult: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, List["UpdatesPackageInfo"]]]:
    """Gets available packages

     Requires authentication as user

    Args:
        package_type (Union[Unset, None, str]):
        target_systems (Union[Unset, None, str]):
        is_premium (Union[Unset, None, bool]):
        is_adult (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['UpdatesPackageInfo']]
    """

    return sync_detailed(
        client=client,
        package_type=package_type,
        target_systems=target_systems,
        is_premium=is_premium,
        is_adult=is_adult,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    package_type: Union[Unset, None, str] = UNSET,
    target_systems: Union[Unset, None, str] = UNSET,
    is_premium: Union[Unset, None, bool] = UNSET,
    is_adult: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, List["UpdatesPackageInfo"]]]:
    """Gets available packages

     Requires authentication as user

    Args:
        package_type (Union[Unset, None, str]):
        target_systems (Union[Unset, None, str]):
        is_premium (Union[Unset, None, bool]):
        is_adult (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['UpdatesPackageInfo']]]
    """

    kwargs = _get_kwargs(
        client=client,
        package_type=package_type,
        target_systems=target_systems,
        is_premium=is_premium,
        is_adult=is_adult,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    package_type: Union[Unset, None, str] = UNSET,
    target_systems: Union[Unset, None, str] = UNSET,
    is_premium: Union[Unset, None, bool] = UNSET,
    is_adult: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, List["UpdatesPackageInfo"]]]:
    """Gets available packages

     Requires authentication as user

    Args:
        package_type (Union[Unset, None, str]):
        target_systems (Union[Unset, None, str]):
        is_premium (Union[Unset, None, bool]):
        is_adult (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['UpdatesPackageInfo']]
    """

    return (
        await asyncio_detailed(
            client=client,
            package_type=package_type,
            target_systems=target_systems,
            is_premium=is_premium,
            is_adult=is_adult,
        )
    ).parsed
