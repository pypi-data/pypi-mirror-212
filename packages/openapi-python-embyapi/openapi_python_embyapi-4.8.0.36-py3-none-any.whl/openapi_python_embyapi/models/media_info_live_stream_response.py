from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.media_source_info import MediaSourceInfo


T = TypeVar("T", bound="MediaInfoLiveStreamResponse")


@attr.s(auto_attribs=True)
class MediaInfoLiveStreamResponse:
    """
    Attributes:
        media_source (Union[Unset, MediaSourceInfo]):
    """

    media_source: Union[Unset, "MediaSourceInfo"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        media_source: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.media_source, Unset):
            media_source = self.media_source.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if media_source is not UNSET:
            field_dict["MediaSource"] = media_source

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.media_source_info import MediaSourceInfo

        d = src_dict.copy()
        _media_source = d.pop("MediaSource", UNSET)
        media_source: Union[Unset, MediaSourceInfo]
        if isinstance(_media_source, Unset):
            media_source = UNSET
        else:
            media_source = MediaSourceInfo.from_dict(_media_source)

        media_info_live_stream_response = cls(
            media_source=media_source,
        )

        media_info_live_stream_response.additional_properties = d
        return media_info_live_stream_response

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
