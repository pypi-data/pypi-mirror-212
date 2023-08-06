from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dlna_subtitle_delivery_method import DlnaSubtitleDeliveryMethod
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: AuthenticatedClient,
    device_profile_id: Union[Unset, None, str] = UNSET,
    device_id: Union[Unset, None, str] = UNSET,
    container: str,
    audio_codec: Union[Unset, None, str] = UNSET,
    enable_auto_stream_copy: Union[Unset, None, bool] = UNSET,
    audio_sample_rate: Union[Unset, None, int] = UNSET,
    audio_bit_rate: Union[Unset, None, int] = UNSET,
    audio_channels: Union[Unset, None, int] = UNSET,
    max_audio_channels: Union[Unset, None, int] = UNSET,
    static: Union[Unset, None, bool] = UNSET,
    profile: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, str] = UNSET,
    framerate: Union[Unset, None, float] = UNSET,
    max_framerate: Union[Unset, None, float] = UNSET,
    copy_timestamps: Union[Unset, None, bool] = UNSET,
    start_time_ticks: Union[Unset, None, int] = UNSET,
    width: Union[Unset, None, int] = UNSET,
    height: Union[Unset, None, int] = UNSET,
    max_width: Union[Unset, None, int] = UNSET,
    max_height: Union[Unset, None, int] = UNSET,
    video_bit_rate: Union[Unset, None, int] = UNSET,
    subtitle_stream_index: Union[Unset, None, int] = UNSET,
    subtitle_method: Union[Unset, None, DlnaSubtitleDeliveryMethod] = UNSET,
    max_ref_frames: Union[Unset, None, int] = UNSET,
    max_video_bit_depth: Union[Unset, None, int] = UNSET,
    video_codec: Union[Unset, None, str] = UNSET,
    audio_stream_index: Union[Unset, None, int] = UNSET,
    video_stream_index: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/Audio/{Id}/stream".format(client.base_url, Id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["DeviceProfileId"] = device_profile_id

    params["DeviceId"] = device_id

    params["Container"] = container

    params["AudioCodec"] = audio_codec

    params["EnableAutoStreamCopy"] = enable_auto_stream_copy

    params["AudioSampleRate"] = audio_sample_rate

    params["AudioBitRate"] = audio_bit_rate

    params["AudioChannels"] = audio_channels

    params["MaxAudioChannels"] = max_audio_channels

    params["Static"] = static

    params["Profile"] = profile

    params["Level"] = level

    params["Framerate"] = framerate

    params["MaxFramerate"] = max_framerate

    params["CopyTimestamps"] = copy_timestamps

    params["StartTimeTicks"] = start_time_ticks

    params["Width"] = width

    params["Height"] = height

    params["MaxWidth"] = max_width

    params["MaxHeight"] = max_height

    params["VideoBitRate"] = video_bit_rate

    params["SubtitleStreamIndex"] = subtitle_stream_index

    json_subtitle_method: Union[Unset, None, str] = UNSET
    if not isinstance(subtitle_method, Unset):
        json_subtitle_method = subtitle_method.value if subtitle_method else None

    params["SubtitleMethod"] = json_subtitle_method

    params["MaxRefFrames"] = max_ref_frames

    params["MaxVideoBitDepth"] = max_video_bit_depth

    params["VideoCodec"] = video_codec

    params["AudioStreamIndex"] = audio_stream_index

    params["VideoStreamIndex"] = video_stream_index

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "head",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
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
    device_profile_id: Union[Unset, None, str] = UNSET,
    device_id: Union[Unset, None, str] = UNSET,
    container: str,
    audio_codec: Union[Unset, None, str] = UNSET,
    enable_auto_stream_copy: Union[Unset, None, bool] = UNSET,
    audio_sample_rate: Union[Unset, None, int] = UNSET,
    audio_bit_rate: Union[Unset, None, int] = UNSET,
    audio_channels: Union[Unset, None, int] = UNSET,
    max_audio_channels: Union[Unset, None, int] = UNSET,
    static: Union[Unset, None, bool] = UNSET,
    profile: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, str] = UNSET,
    framerate: Union[Unset, None, float] = UNSET,
    max_framerate: Union[Unset, None, float] = UNSET,
    copy_timestamps: Union[Unset, None, bool] = UNSET,
    start_time_ticks: Union[Unset, None, int] = UNSET,
    width: Union[Unset, None, int] = UNSET,
    height: Union[Unset, None, int] = UNSET,
    max_width: Union[Unset, None, int] = UNSET,
    max_height: Union[Unset, None, int] = UNSET,
    video_bit_rate: Union[Unset, None, int] = UNSET,
    subtitle_stream_index: Union[Unset, None, int] = UNSET,
    subtitle_method: Union[Unset, None, DlnaSubtitleDeliveryMethod] = UNSET,
    max_ref_frames: Union[Unset, None, int] = UNSET,
    max_video_bit_depth: Union[Unset, None, int] = UNSET,
    video_codec: Union[Unset, None, str] = UNSET,
    audio_stream_index: Union[Unset, None, int] = UNSET,
    video_stream_index: Union[Unset, None, int] = UNSET,
) -> Response[Any]:
    """Gets an audio stream

     Requires authentication as user

    Args:
        id (str):
        device_profile_id (Union[Unset, None, str]):
        device_id (Union[Unset, None, str]):
        container (str):
        audio_codec (Union[Unset, None, str]):
        enable_auto_stream_copy (Union[Unset, None, bool]):
        audio_sample_rate (Union[Unset, None, int]):
        audio_bit_rate (Union[Unset, None, int]):
        audio_channels (Union[Unset, None, int]):
        max_audio_channels (Union[Unset, None, int]):
        static (Union[Unset, None, bool]):
        profile (Union[Unset, None, str]):
        level (Union[Unset, None, str]):
        framerate (Union[Unset, None, float]):
        max_framerate (Union[Unset, None, float]):
        copy_timestamps (Union[Unset, None, bool]):
        start_time_ticks (Union[Unset, None, int]):
        width (Union[Unset, None, int]):
        height (Union[Unset, None, int]):
        max_width (Union[Unset, None, int]):
        max_height (Union[Unset, None, int]):
        video_bit_rate (Union[Unset, None, int]):
        subtitle_stream_index (Union[Unset, None, int]):
        subtitle_method (Union[Unset, None, DlnaSubtitleDeliveryMethod]):
        max_ref_frames (Union[Unset, None, int]):
        max_video_bit_depth (Union[Unset, None, int]):
        video_codec (Union[Unset, None, str]):
        audio_stream_index (Union[Unset, None, int]):
        video_stream_index (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        device_profile_id=device_profile_id,
        device_id=device_id,
        container=container,
        audio_codec=audio_codec,
        enable_auto_stream_copy=enable_auto_stream_copy,
        audio_sample_rate=audio_sample_rate,
        audio_bit_rate=audio_bit_rate,
        audio_channels=audio_channels,
        max_audio_channels=max_audio_channels,
        static=static,
        profile=profile,
        level=level,
        framerate=framerate,
        max_framerate=max_framerate,
        copy_timestamps=copy_timestamps,
        start_time_ticks=start_time_ticks,
        width=width,
        height=height,
        max_width=max_width,
        max_height=max_height,
        video_bit_rate=video_bit_rate,
        subtitle_stream_index=subtitle_stream_index,
        subtitle_method=subtitle_method,
        max_ref_frames=max_ref_frames,
        max_video_bit_depth=max_video_bit_depth,
        video_codec=video_codec,
        audio_stream_index=audio_stream_index,
        video_stream_index=video_stream_index,
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
    device_profile_id: Union[Unset, None, str] = UNSET,
    device_id: Union[Unset, None, str] = UNSET,
    container: str,
    audio_codec: Union[Unset, None, str] = UNSET,
    enable_auto_stream_copy: Union[Unset, None, bool] = UNSET,
    audio_sample_rate: Union[Unset, None, int] = UNSET,
    audio_bit_rate: Union[Unset, None, int] = UNSET,
    audio_channels: Union[Unset, None, int] = UNSET,
    max_audio_channels: Union[Unset, None, int] = UNSET,
    static: Union[Unset, None, bool] = UNSET,
    profile: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, str] = UNSET,
    framerate: Union[Unset, None, float] = UNSET,
    max_framerate: Union[Unset, None, float] = UNSET,
    copy_timestamps: Union[Unset, None, bool] = UNSET,
    start_time_ticks: Union[Unset, None, int] = UNSET,
    width: Union[Unset, None, int] = UNSET,
    height: Union[Unset, None, int] = UNSET,
    max_width: Union[Unset, None, int] = UNSET,
    max_height: Union[Unset, None, int] = UNSET,
    video_bit_rate: Union[Unset, None, int] = UNSET,
    subtitle_stream_index: Union[Unset, None, int] = UNSET,
    subtitle_method: Union[Unset, None, DlnaSubtitleDeliveryMethod] = UNSET,
    max_ref_frames: Union[Unset, None, int] = UNSET,
    max_video_bit_depth: Union[Unset, None, int] = UNSET,
    video_codec: Union[Unset, None, str] = UNSET,
    audio_stream_index: Union[Unset, None, int] = UNSET,
    video_stream_index: Union[Unset, None, int] = UNSET,
) -> Response[Any]:
    """Gets an audio stream

     Requires authentication as user

    Args:
        id (str):
        device_profile_id (Union[Unset, None, str]):
        device_id (Union[Unset, None, str]):
        container (str):
        audio_codec (Union[Unset, None, str]):
        enable_auto_stream_copy (Union[Unset, None, bool]):
        audio_sample_rate (Union[Unset, None, int]):
        audio_bit_rate (Union[Unset, None, int]):
        audio_channels (Union[Unset, None, int]):
        max_audio_channels (Union[Unset, None, int]):
        static (Union[Unset, None, bool]):
        profile (Union[Unset, None, str]):
        level (Union[Unset, None, str]):
        framerate (Union[Unset, None, float]):
        max_framerate (Union[Unset, None, float]):
        copy_timestamps (Union[Unset, None, bool]):
        start_time_ticks (Union[Unset, None, int]):
        width (Union[Unset, None, int]):
        height (Union[Unset, None, int]):
        max_width (Union[Unset, None, int]):
        max_height (Union[Unset, None, int]):
        video_bit_rate (Union[Unset, None, int]):
        subtitle_stream_index (Union[Unset, None, int]):
        subtitle_method (Union[Unset, None, DlnaSubtitleDeliveryMethod]):
        max_ref_frames (Union[Unset, None, int]):
        max_video_bit_depth (Union[Unset, None, int]):
        video_codec (Union[Unset, None, str]):
        audio_stream_index (Union[Unset, None, int]):
        video_stream_index (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        device_profile_id=device_profile_id,
        device_id=device_id,
        container=container,
        audio_codec=audio_codec,
        enable_auto_stream_copy=enable_auto_stream_copy,
        audio_sample_rate=audio_sample_rate,
        audio_bit_rate=audio_bit_rate,
        audio_channels=audio_channels,
        max_audio_channels=max_audio_channels,
        static=static,
        profile=profile,
        level=level,
        framerate=framerate,
        max_framerate=max_framerate,
        copy_timestamps=copy_timestamps,
        start_time_ticks=start_time_ticks,
        width=width,
        height=height,
        max_width=max_width,
        max_height=max_height,
        video_bit_rate=video_bit_rate,
        subtitle_stream_index=subtitle_stream_index,
        subtitle_method=subtitle_method,
        max_ref_frames=max_ref_frames,
        max_video_bit_depth=max_video_bit_depth,
        video_codec=video_codec,
        audio_stream_index=audio_stream_index,
        video_stream_index=video_stream_index,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
