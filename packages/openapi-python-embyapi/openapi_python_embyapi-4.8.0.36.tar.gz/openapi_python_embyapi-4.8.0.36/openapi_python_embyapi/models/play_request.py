from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlayRequest")


@attr.s(auto_attribs=True)
class PlayRequest:
    """
    Attributes:
        controlling_user_id (Union[Unset, str]):
        subtitle_stream_index (Union[Unset, None, int]):
        audio_stream_index (Union[Unset, None, int]):
        media_source_id (Union[Unset, str]):
        start_index (Union[Unset, None, int]):
    """

    controlling_user_id: Union[Unset, str] = UNSET
    subtitle_stream_index: Union[Unset, None, int] = UNSET
    audio_stream_index: Union[Unset, None, int] = UNSET
    media_source_id: Union[Unset, str] = UNSET
    start_index: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        controlling_user_id = self.controlling_user_id
        subtitle_stream_index = self.subtitle_stream_index
        audio_stream_index = self.audio_stream_index
        media_source_id = self.media_source_id
        start_index = self.start_index

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if controlling_user_id is not UNSET:
            field_dict["ControllingUserId"] = controlling_user_id
        if subtitle_stream_index is not UNSET:
            field_dict["SubtitleStreamIndex"] = subtitle_stream_index
        if audio_stream_index is not UNSET:
            field_dict["AudioStreamIndex"] = audio_stream_index
        if media_source_id is not UNSET:
            field_dict["MediaSourceId"] = media_source_id
        if start_index is not UNSET:
            field_dict["StartIndex"] = start_index

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        controlling_user_id = d.pop("ControllingUserId", UNSET)

        subtitle_stream_index = d.pop("SubtitleStreamIndex", UNSET)

        audio_stream_index = d.pop("AudioStreamIndex", UNSET)

        media_source_id = d.pop("MediaSourceId", UNSET)

        start_index = d.pop("StartIndex", UNSET)

        play_request = cls(
            controlling_user_id=controlling_user_id,
            subtitle_stream_index=subtitle_stream_index,
            audio_stream_index=audio_stream_index,
            media_source_id=media_source_id,
            start_index=start_index,
        )

        play_request.additional_properties = d
        return play_request

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
