from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dlna_playback_error_code import DlnaPlaybackErrorCode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.media_source_info import MediaSourceInfo


T = TypeVar("T", bound="MediaInfoPlaybackInfoResponse")


@attr.s(auto_attribs=True)
class MediaInfoPlaybackInfoResponse:
    """
    Attributes:
        media_sources (Union[Unset, List['MediaSourceInfo']]):
        play_session_id (Union[Unset, str]):
        error_code (Union[Unset, DlnaPlaybackErrorCode]):
    """

    media_sources: Union[Unset, List["MediaSourceInfo"]] = UNSET
    play_session_id: Union[Unset, str] = UNSET
    error_code: Union[Unset, DlnaPlaybackErrorCode] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        media_sources: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.media_sources, Unset):
            media_sources = []
            for media_sources_item_data in self.media_sources:
                media_sources_item = media_sources_item_data.to_dict()

                media_sources.append(media_sources_item)

        play_session_id = self.play_session_id
        error_code: Union[Unset, str] = UNSET
        if not isinstance(self.error_code, Unset):
            error_code = self.error_code.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if media_sources is not UNSET:
            field_dict["MediaSources"] = media_sources
        if play_session_id is not UNSET:
            field_dict["PlaySessionId"] = play_session_id
        if error_code is not UNSET:
            field_dict["ErrorCode"] = error_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.media_source_info import MediaSourceInfo

        d = src_dict.copy()
        media_sources = []
        _media_sources = d.pop("MediaSources", UNSET)
        for media_sources_item_data in _media_sources or []:
            media_sources_item = MediaSourceInfo.from_dict(media_sources_item_data)

            media_sources.append(media_sources_item)

        play_session_id = d.pop("PlaySessionId", UNSET)

        _error_code = d.pop("ErrorCode", UNSET)
        error_code: Union[Unset, DlnaPlaybackErrorCode]
        if isinstance(_error_code, Unset):
            error_code = UNSET
        else:
            error_code = DlnaPlaybackErrorCode(_error_code)

        media_info_playback_info_response = cls(
            media_sources=media_sources,
            play_session_id=play_session_id,
            error_code=error_code,
        )

        media_info_playback_info_response.additional_properties = d
        return media_info_playback_info_response

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
