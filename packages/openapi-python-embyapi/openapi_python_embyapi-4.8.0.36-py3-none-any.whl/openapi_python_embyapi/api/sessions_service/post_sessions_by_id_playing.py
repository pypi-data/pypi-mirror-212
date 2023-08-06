from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.play_command import PlayCommand
from ...models.play_request import PlayRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: PlayRequest,
    item_ids: List[int],
    start_position_ticks: Union[Unset, None, int] = UNSET,
    play_command: PlayCommand,
) -> Dict[str, Any]:
    url = "{}/Sessions/{Id}/Playing".format(client.base_url, Id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_item_ids = item_ids

    params["ItemIds"] = json_item_ids

    params["StartPositionTicks"] = start_position_ticks

    json_play_command = play_command.value

    params["PlayCommand"] = json_play_command

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
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
    json_body: PlayRequest,
    item_ids: List[int],
    start_position_ticks: Union[Unset, None, int] = UNSET,
    play_command: PlayCommand,
) -> Response[Any]:
    """Instructs a session to play an item

     Requires authentication as user

    Args:
        id (str):
        item_ids (List[int]):
        start_position_ticks (Union[Unset, None, int]):
        play_command (PlayCommand):
        json_body (PlayRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
        item_ids=item_ids,
        start_position_ticks=start_position_ticks,
        play_command=play_command,
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
    json_body: PlayRequest,
    item_ids: List[int],
    start_position_ticks: Union[Unset, None, int] = UNSET,
    play_command: PlayCommand,
) -> Response[Any]:
    """Instructs a session to play an item

     Requires authentication as user

    Args:
        id (str):
        item_ids (List[int]):
        start_position_ticks (Union[Unset, None, int]):
        play_command (PlayCommand):
        json_body (PlayRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
        item_ids=item_ids,
        start_position_ticks=start_position_ticks,
        play_command=play_command,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
