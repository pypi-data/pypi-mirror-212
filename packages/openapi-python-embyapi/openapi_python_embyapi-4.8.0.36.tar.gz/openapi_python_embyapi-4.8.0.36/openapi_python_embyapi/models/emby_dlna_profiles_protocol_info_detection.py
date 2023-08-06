from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmbyDlnaProfilesProtocolInfoDetection")


@attr.s(auto_attribs=True)
class EmbyDlnaProfilesProtocolInfoDetection:
    """
    Attributes:
        enabled_for_video (Union[Unset, bool]):
        enabled_for_audio (Union[Unset, bool]):
        enabled_for_photos (Union[Unset, bool]):
    """

    enabled_for_video: Union[Unset, bool] = UNSET
    enabled_for_audio: Union[Unset, bool] = UNSET
    enabled_for_photos: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enabled_for_video = self.enabled_for_video
        enabled_for_audio = self.enabled_for_audio
        enabled_for_photos = self.enabled_for_photos

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled_for_video is not UNSET:
            field_dict["EnabledForVideo"] = enabled_for_video
        if enabled_for_audio is not UNSET:
            field_dict["EnabledForAudio"] = enabled_for_audio
        if enabled_for_photos is not UNSET:
            field_dict["EnabledForPhotos"] = enabled_for_photos

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enabled_for_video = d.pop("EnabledForVideo", UNSET)

        enabled_for_audio = d.pop("EnabledForAudio", UNSET)

        enabled_for_photos = d.pop("EnabledForPhotos", UNSET)

        emby_dlna_profiles_protocol_info_detection = cls(
            enabled_for_video=enabled_for_video,
            enabled_for_audio=enabled_for_audio,
            enabled_for_photos=enabled_for_photos,
        )

        emby_dlna_profiles_protocol_info_detection.additional_properties = d
        return emby_dlna_profiles_protocol_info_detection

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
