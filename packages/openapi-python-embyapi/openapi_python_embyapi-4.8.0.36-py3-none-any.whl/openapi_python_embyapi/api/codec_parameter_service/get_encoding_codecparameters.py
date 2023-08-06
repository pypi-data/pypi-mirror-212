from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.emby_web_generic_edit_edit_object_container import EmbyWebGenericEditEditObjectContainer
from ...models.media_encoding_codec_parameter_context import MediaEncodingCodecParameterContext
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    codec_id: str,
    parameter_context: MediaEncodingCodecParameterContext,
) -> Dict[str, Any]:
    url = "{}/Encoding/CodecParameters".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["CodecId"] = codec_id

    json_parameter_context = parameter_context.value

    params["ParameterContext"] = json_parameter_context

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
) -> Optional[Union[Any, EmbyWebGenericEditEditObjectContainer]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = EmbyWebGenericEditEditObjectContainer.from_dict(response.json())

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
) -> Response[Union[Any, EmbyWebGenericEditEditObjectContainer]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    codec_id: str,
    parameter_context: MediaEncodingCodecParameterContext,
) -> Response[Union[Any, EmbyWebGenericEditEditObjectContainer]]:
    """Gets the parameters for a specified codec.

     Requires authentication as user

    Args:
        codec_id (str):
        parameter_context (MediaEncodingCodecParameterContext):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, EmbyWebGenericEditEditObjectContainer]]
    """

    kwargs = _get_kwargs(
        client=client,
        codec_id=codec_id,
        parameter_context=parameter_context,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    codec_id: str,
    parameter_context: MediaEncodingCodecParameterContext,
) -> Optional[Union[Any, EmbyWebGenericEditEditObjectContainer]]:
    """Gets the parameters for a specified codec.

     Requires authentication as user

    Args:
        codec_id (str):
        parameter_context (MediaEncodingCodecParameterContext):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, EmbyWebGenericEditEditObjectContainer]
    """

    return sync_detailed(
        client=client,
        codec_id=codec_id,
        parameter_context=parameter_context,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    codec_id: str,
    parameter_context: MediaEncodingCodecParameterContext,
) -> Response[Union[Any, EmbyWebGenericEditEditObjectContainer]]:
    """Gets the parameters for a specified codec.

     Requires authentication as user

    Args:
        codec_id (str):
        parameter_context (MediaEncodingCodecParameterContext):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, EmbyWebGenericEditEditObjectContainer]]
    """

    kwargs = _get_kwargs(
        client=client,
        codec_id=codec_id,
        parameter_context=parameter_context,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    codec_id: str,
    parameter_context: MediaEncodingCodecParameterContext,
) -> Optional[Union[Any, EmbyWebGenericEditEditObjectContainer]]:
    """Gets the parameters for a specified codec.

     Requires authentication as user

    Args:
        codec_id (str):
        parameter_context (MediaEncodingCodecParameterContext):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, EmbyWebGenericEditEditObjectContainer]
    """

    return (
        await asyncio_detailed(
            client=client,
            codec_id=codec_id,
            parameter_context=parameter_context,
        )
    ).parsed
