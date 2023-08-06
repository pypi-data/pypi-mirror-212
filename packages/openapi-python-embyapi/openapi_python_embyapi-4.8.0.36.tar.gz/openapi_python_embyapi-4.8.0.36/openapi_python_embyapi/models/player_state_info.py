from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.play_method import PlayMethod
from ..models.repeat_mode import RepeatMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="PlayerStateInfo")


@attr.s(auto_attribs=True)
class PlayerStateInfo:
    """
    Attributes:
        position_ticks (Union[Unset, None, int]):
        can_seek (Union[Unset, bool]):
        is_paused (Union[Unset, bool]):
        is_muted (Union[Unset, bool]):
        volume_level (Union[Unset, None, int]):
        audio_stream_index (Union[Unset, None, int]):
        subtitle_stream_index (Union[Unset, None, int]):
        media_source_id (Union[Unset, str]):
        play_method (Union[Unset, PlayMethod]):
        repeat_mode (Union[Unset, RepeatMode]):
        subtitle_offset (Union[Unset, int]):
        playback_rate (Union[Unset, float]):
    """

    position_ticks: Union[Unset, None, int] = UNSET
    can_seek: Union[Unset, bool] = UNSET
    is_paused: Union[Unset, bool] = UNSET
    is_muted: Union[Unset, bool] = UNSET
    volume_level: Union[Unset, None, int] = UNSET
    audio_stream_index: Union[Unset, None, int] = UNSET
    subtitle_stream_index: Union[Unset, None, int] = UNSET
    media_source_id: Union[Unset, str] = UNSET
    play_method: Union[Unset, PlayMethod] = UNSET
    repeat_mode: Union[Unset, RepeatMode] = UNSET
    subtitle_offset: Union[Unset, int] = UNSET
    playback_rate: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        position_ticks = self.position_ticks
        can_seek = self.can_seek
        is_paused = self.is_paused
        is_muted = self.is_muted
        volume_level = self.volume_level
        audio_stream_index = self.audio_stream_index
        subtitle_stream_index = self.subtitle_stream_index
        media_source_id = self.media_source_id
        play_method: Union[Unset, str] = UNSET
        if not isinstance(self.play_method, Unset):
            play_method = self.play_method.value

        repeat_mode: Union[Unset, str] = UNSET
        if not isinstance(self.repeat_mode, Unset):
            repeat_mode = self.repeat_mode.value

        subtitle_offset = self.subtitle_offset
        playback_rate = self.playback_rate

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if position_ticks is not UNSET:
            field_dict["PositionTicks"] = position_ticks
        if can_seek is not UNSET:
            field_dict["CanSeek"] = can_seek
        if is_paused is not UNSET:
            field_dict["IsPaused"] = is_paused
        if is_muted is not UNSET:
            field_dict["IsMuted"] = is_muted
        if volume_level is not UNSET:
            field_dict["VolumeLevel"] = volume_level
        if audio_stream_index is not UNSET:
            field_dict["AudioStreamIndex"] = audio_stream_index
        if subtitle_stream_index is not UNSET:
            field_dict["SubtitleStreamIndex"] = subtitle_stream_index
        if media_source_id is not UNSET:
            field_dict["MediaSourceId"] = media_source_id
        if play_method is not UNSET:
            field_dict["PlayMethod"] = play_method
        if repeat_mode is not UNSET:
            field_dict["RepeatMode"] = repeat_mode
        if subtitle_offset is not UNSET:
            field_dict["SubtitleOffset"] = subtitle_offset
        if playback_rate is not UNSET:
            field_dict["PlaybackRate"] = playback_rate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        position_ticks = d.pop("PositionTicks", UNSET)

        can_seek = d.pop("CanSeek", UNSET)

        is_paused = d.pop("IsPaused", UNSET)

        is_muted = d.pop("IsMuted", UNSET)

        volume_level = d.pop("VolumeLevel", UNSET)

        audio_stream_index = d.pop("AudioStreamIndex", UNSET)

        subtitle_stream_index = d.pop("SubtitleStreamIndex", UNSET)

        media_source_id = d.pop("MediaSourceId", UNSET)

        _play_method = d.pop("PlayMethod", UNSET)
        play_method: Union[Unset, PlayMethod]
        if isinstance(_play_method, Unset):
            play_method = UNSET
        else:
            play_method = PlayMethod(_play_method)

        _repeat_mode = d.pop("RepeatMode", UNSET)
        repeat_mode: Union[Unset, RepeatMode]
        if isinstance(_repeat_mode, Unset):
            repeat_mode = UNSET
        else:
            repeat_mode = RepeatMode(_repeat_mode)

        subtitle_offset = d.pop("SubtitleOffset", UNSET)

        playback_rate = d.pop("PlaybackRate", UNSET)

        player_state_info = cls(
            position_ticks=position_ticks,
            can_seek=can_seek,
            is_paused=is_paused,
            is_muted=is_muted,
            volume_level=volume_level,
            audio_stream_index=audio_stream_index,
            subtitle_stream_index=subtitle_stream_index,
            media_source_id=media_source_id,
            play_method=play_method,
            repeat_mode=repeat_mode,
            subtitle_offset=subtitle_offset,
            playback_rate=playback_rate,
        )

        player_state_info.additional_properties = d
        return player_state_info

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
