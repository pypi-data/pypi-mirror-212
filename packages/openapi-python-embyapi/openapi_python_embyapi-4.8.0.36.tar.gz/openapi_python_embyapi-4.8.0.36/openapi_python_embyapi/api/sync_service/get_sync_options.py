from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sync_model_sync_dialog_options import SyncModelSyncDialogOptions
from ...models.sync_sync_category import SyncSyncCategory
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    user_id: str,
    item_ids: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    target_id: Union[Unset, None, str] = UNSET,
    category: Union[Unset, None, SyncSyncCategory] = UNSET,
) -> Dict[str, Any]:
    url = "{}/Sync/Options".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["UserId"] = user_id

    params["ItemIds"] = item_ids

    params["ParentId"] = parent_id

    params["TargetId"] = target_id

    json_category: Union[Unset, None, str] = UNSET
    if not isinstance(category, Unset):
        json_category = category.value if category else None

    params["Category"] = json_category

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, SyncModelSyncDialogOptions]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SyncModelSyncDialogOptions.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, SyncModelSyncDialogOptions]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    user_id: str,
    item_ids: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    target_id: Union[Unset, None, str] = UNSET,
    category: Union[Unset, None, SyncSyncCategory] = UNSET,
) -> Response[Union[Any, SyncModelSyncDialogOptions]]:
    """Gets a list of available sync targets.

     Requires authentication as user

    Args:
        user_id (str):
        item_ids (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        target_id (Union[Unset, None, str]):
        category (Union[Unset, None, SyncSyncCategory]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SyncModelSyncDialogOptions]]
    """

    kwargs = _get_kwargs(
        client=client,
        user_id=user_id,
        item_ids=item_ids,
        parent_id=parent_id,
        target_id=target_id,
        category=category,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    user_id: str,
    item_ids: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    target_id: Union[Unset, None, str] = UNSET,
    category: Union[Unset, None, SyncSyncCategory] = UNSET,
) -> Optional[Union[Any, SyncModelSyncDialogOptions]]:
    """Gets a list of available sync targets.

     Requires authentication as user

    Args:
        user_id (str):
        item_ids (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        target_id (Union[Unset, None, str]):
        category (Union[Unset, None, SyncSyncCategory]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SyncModelSyncDialogOptions]
    """

    return sync_detailed(
        client=client,
        user_id=user_id,
        item_ids=item_ids,
        parent_id=parent_id,
        target_id=target_id,
        category=category,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    user_id: str,
    item_ids: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    target_id: Union[Unset, None, str] = UNSET,
    category: Union[Unset, None, SyncSyncCategory] = UNSET,
) -> Response[Union[Any, SyncModelSyncDialogOptions]]:
    """Gets a list of available sync targets.

     Requires authentication as user

    Args:
        user_id (str):
        item_ids (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        target_id (Union[Unset, None, str]):
        category (Union[Unset, None, SyncSyncCategory]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SyncModelSyncDialogOptions]]
    """

    kwargs = _get_kwargs(
        client=client,
        user_id=user_id,
        item_ids=item_ids,
        parent_id=parent_id,
        target_id=target_id,
        category=category,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    user_id: str,
    item_ids: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    target_id: Union[Unset, None, str] = UNSET,
    category: Union[Unset, None, SyncSyncCategory] = UNSET,
) -> Optional[Union[Any, SyncModelSyncDialogOptions]]:
    """Gets a list of available sync targets.

     Requires authentication as user

    Args:
        user_id (str):
        item_ids (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        target_id (Union[Unset, None, str]):
        category (Union[Unset, None, SyncSyncCategory]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SyncModelSyncDialogOptions]
    """

    return (
        await asyncio_detailed(
            client=client,
            user_id=user_id,
            item_ids=item_ids,
            parent_id=parent_id,
            target_id=target_id,
            category=category,
        )
    ).parsed
