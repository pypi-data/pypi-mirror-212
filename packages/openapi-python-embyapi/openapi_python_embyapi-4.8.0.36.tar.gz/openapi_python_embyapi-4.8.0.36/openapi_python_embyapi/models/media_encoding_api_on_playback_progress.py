from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.progress_event import ProgressEvent
from ..types import UNSET, Unset

T = TypeVar("T", bound="MediaEncodingApiOnPlaybackProgress")


@attr.s(auto_attribs=True)
class MediaEncodingApiOnPlaybackProgress:
    """
    Attributes:
        playlist_index (Union[Unset, int]):
        playlist_length (Union[Unset, int]):
        event_name (Union[Unset, ProgressEvent]):
    """

    playlist_index: Union[Unset, int] = UNSET
    playlist_length: Union[Unset, int] = UNSET
    event_name: Union[Unset, ProgressEvent] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        playlist_index = self.playlist_index
        playlist_length = self.playlist_length
        event_name: Union[Unset, str] = UNSET
        if not isinstance(self.event_name, Unset):
            event_name = self.event_name.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if playlist_index is not UNSET:
            field_dict["PlaylistIndex"] = playlist_index
        if playlist_length is not UNSET:
            field_dict["PlaylistLength"] = playlist_length
        if event_name is not UNSET:
            field_dict["EventName"] = event_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        playlist_index = d.pop("PlaylistIndex", UNSET)

        playlist_length = d.pop("PlaylistLength", UNSET)

        _event_name = d.pop("EventName", UNSET)
        event_name: Union[Unset, ProgressEvent]
        if isinstance(_event_name, Unset):
            event_name = UNSET
        else:
            event_name = ProgressEvent(_event_name)

        media_encoding_api_on_playback_progress = cls(
            playlist_index=playlist_index,
            playlist_length=playlist_length,
            event_name=event_name,
        )

        media_encoding_api_on_playback_progress.additional_properties = d
        return media_encoding_api_on_playback_progress

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
