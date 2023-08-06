from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.media_info_media_protocol import MediaInfoMediaProtocol
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dlna_device_profile import DlnaDeviceProfile


T = TypeVar("T", bound="MediaInfoLiveStreamRequest")


@attr.s(auto_attribs=True)
class MediaInfoLiveStreamRequest:
    """
    Attributes:
        open_token (Union[Unset, str]):
        user_id (Union[Unset, str]):
        play_session_id (Union[Unset, str]):
        max_streaming_bitrate (Union[Unset, None, int]):
        start_time_ticks (Union[Unset, None, int]):
        audio_stream_index (Union[Unset, None, int]):
        subtitle_stream_index (Union[Unset, None, int]):
        max_audio_channels (Union[Unset, None, int]):
        item_id (Union[Unset, int]):
        device_profile (Union[Unset, DlnaDeviceProfile]):
        enable_direct_play (Union[Unset, bool]):
        enable_direct_stream (Union[Unset, bool]):
        enable_transcoding (Union[Unset, bool]):
        allow_video_stream_copy (Union[Unset, bool]):
        allow_interlaced_video_stream_copy (Union[Unset, bool]):
        allow_audio_stream_copy (Union[Unset, bool]):
        direct_play_protocols (Union[Unset, List[MediaInfoMediaProtocol]]):
    """

    open_token: Union[Unset, str] = UNSET
    user_id: Union[Unset, str] = UNSET
    play_session_id: Union[Unset, str] = UNSET
    max_streaming_bitrate: Union[Unset, None, int] = UNSET
    start_time_ticks: Union[Unset, None, int] = UNSET
    audio_stream_index: Union[Unset, None, int] = UNSET
    subtitle_stream_index: Union[Unset, None, int] = UNSET
    max_audio_channels: Union[Unset, None, int] = UNSET
    item_id: Union[Unset, int] = UNSET
    device_profile: Union[Unset, "DlnaDeviceProfile"] = UNSET
    enable_direct_play: Union[Unset, bool] = UNSET
    enable_direct_stream: Union[Unset, bool] = UNSET
    enable_transcoding: Union[Unset, bool] = UNSET
    allow_video_stream_copy: Union[Unset, bool] = UNSET
    allow_interlaced_video_stream_copy: Union[Unset, bool] = UNSET
    allow_audio_stream_copy: Union[Unset, bool] = UNSET
    direct_play_protocols: Union[Unset, List[MediaInfoMediaProtocol]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        open_token = self.open_token
        user_id = self.user_id
        play_session_id = self.play_session_id
        max_streaming_bitrate = self.max_streaming_bitrate
        start_time_ticks = self.start_time_ticks
        audio_stream_index = self.audio_stream_index
        subtitle_stream_index = self.subtitle_stream_index
        max_audio_channels = self.max_audio_channels
        item_id = self.item_id
        device_profile: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.device_profile, Unset):
            device_profile = self.device_profile.to_dict()

        enable_direct_play = self.enable_direct_play
        enable_direct_stream = self.enable_direct_stream
        enable_transcoding = self.enable_transcoding
        allow_video_stream_copy = self.allow_video_stream_copy
        allow_interlaced_video_stream_copy = self.allow_interlaced_video_stream_copy
        allow_audio_stream_copy = self.allow_audio_stream_copy
        direct_play_protocols: Union[Unset, List[str]] = UNSET
        if not isinstance(self.direct_play_protocols, Unset):
            direct_play_protocols = []
            for direct_play_protocols_item_data in self.direct_play_protocols:
                direct_play_protocols_item = direct_play_protocols_item_data.value

                direct_play_protocols.append(direct_play_protocols_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if open_token is not UNSET:
            field_dict["OpenToken"] = open_token
        if user_id is not UNSET:
            field_dict["UserId"] = user_id
        if play_session_id is not UNSET:
            field_dict["PlaySessionId"] = play_session_id
        if max_streaming_bitrate is not UNSET:
            field_dict["MaxStreamingBitrate"] = max_streaming_bitrate
        if start_time_ticks is not UNSET:
            field_dict["StartTimeTicks"] = start_time_ticks
        if audio_stream_index is not UNSET:
            field_dict["AudioStreamIndex"] = audio_stream_index
        if subtitle_stream_index is not UNSET:
            field_dict["SubtitleStreamIndex"] = subtitle_stream_index
        if max_audio_channels is not UNSET:
            field_dict["MaxAudioChannels"] = max_audio_channels
        if item_id is not UNSET:
            field_dict["ItemId"] = item_id
        if device_profile is not UNSET:
            field_dict["DeviceProfile"] = device_profile
        if enable_direct_play is not UNSET:
            field_dict["EnableDirectPlay"] = enable_direct_play
        if enable_direct_stream is not UNSET:
            field_dict["EnableDirectStream"] = enable_direct_stream
        if enable_transcoding is not UNSET:
            field_dict["EnableTranscoding"] = enable_transcoding
        if allow_video_stream_copy is not UNSET:
            field_dict["AllowVideoStreamCopy"] = allow_video_stream_copy
        if allow_interlaced_video_stream_copy is not UNSET:
            field_dict["AllowInterlacedVideoStreamCopy"] = allow_interlaced_video_stream_copy
        if allow_audio_stream_copy is not UNSET:
            field_dict["AllowAudioStreamCopy"] = allow_audio_stream_copy
        if direct_play_protocols is not UNSET:
            field_dict["DirectPlayProtocols"] = direct_play_protocols

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dlna_device_profile import DlnaDeviceProfile

        d = src_dict.copy()
        open_token = d.pop("OpenToken", UNSET)

        user_id = d.pop("UserId", UNSET)

        play_session_id = d.pop("PlaySessionId", UNSET)

        max_streaming_bitrate = d.pop("MaxStreamingBitrate", UNSET)

        start_time_ticks = d.pop("StartTimeTicks", UNSET)

        audio_stream_index = d.pop("AudioStreamIndex", UNSET)

        subtitle_stream_index = d.pop("SubtitleStreamIndex", UNSET)

        max_audio_channels = d.pop("MaxAudioChannels", UNSET)

        item_id = d.pop("ItemId", UNSET)

        _device_profile = d.pop("DeviceProfile", UNSET)
        device_profile: Union[Unset, DlnaDeviceProfile]
        if isinstance(_device_profile, Unset):
            device_profile = UNSET
        else:
            device_profile = DlnaDeviceProfile.from_dict(_device_profile)

        enable_direct_play = d.pop("EnableDirectPlay", UNSET)

        enable_direct_stream = d.pop("EnableDirectStream", UNSET)

        enable_transcoding = d.pop("EnableTranscoding", UNSET)

        allow_video_stream_copy = d.pop("AllowVideoStreamCopy", UNSET)

        allow_interlaced_video_stream_copy = d.pop("AllowInterlacedVideoStreamCopy", UNSET)

        allow_audio_stream_copy = d.pop("AllowAudioStreamCopy", UNSET)

        direct_play_protocols = []
        _direct_play_protocols = d.pop("DirectPlayProtocols", UNSET)
        for direct_play_protocols_item_data in _direct_play_protocols or []:
            direct_play_protocols_item = MediaInfoMediaProtocol(direct_play_protocols_item_data)

            direct_play_protocols.append(direct_play_protocols_item)

        media_info_live_stream_request = cls(
            open_token=open_token,
            user_id=user_id,
            play_session_id=play_session_id,
            max_streaming_bitrate=max_streaming_bitrate,
            start_time_ticks=start_time_ticks,
            audio_stream_index=audio_stream_index,
            subtitle_stream_index=subtitle_stream_index,
            max_audio_channels=max_audio_channels,
            item_id=item_id,
            device_profile=device_profile,
            enable_direct_play=enable_direct_play,
            enable_direct_stream=enable_direct_stream,
            enable_transcoding=enable_transcoding,
            allow_video_stream_copy=allow_video_stream_copy,
            allow_interlaced_video_stream_copy=allow_interlaced_video_stream_copy,
            allow_audio_stream_copy=allow_audio_stream_copy,
            direct_play_protocols=direct_play_protocols,
        )

        media_info_live_stream_request.additional_properties = d
        return media_info_live_stream_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
