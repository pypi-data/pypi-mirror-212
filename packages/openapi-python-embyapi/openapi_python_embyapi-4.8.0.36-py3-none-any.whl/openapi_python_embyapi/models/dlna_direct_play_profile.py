from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dlna_dlna_profile_type import DlnaDlnaProfileType
from ..types import UNSET, Unset

T = TypeVar("T", bound="DlnaDirectPlayProfile")


@attr.s(auto_attribs=True)
class DlnaDirectPlayProfile:
    """
    Attributes:
        container (Union[Unset, str]):
        audio_codec (Union[Unset, str]):
        video_codec (Union[Unset, str]):
        type (Union[Unset, DlnaDlnaProfileType]):
    """

    container: Union[Unset, str] = UNSET
    audio_codec: Union[Unset, str] = UNSET
    video_codec: Union[Unset, str] = UNSET
    type: Union[Unset, DlnaDlnaProfileType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        container = self.container
        audio_codec = self.audio_codec
        video_codec = self.video_codec
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if container is not UNSET:
            field_dict["Container"] = container
        if audio_codec is not UNSET:
            field_dict["AudioCodec"] = audio_codec
        if video_codec is not UNSET:
            field_dict["VideoCodec"] = video_codec
        if type is not UNSET:
            field_dict["Type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        container = d.pop("Container", UNSET)

        audio_codec = d.pop("AudioCodec", UNSET)

        video_codec = d.pop("VideoCodec", UNSET)

        _type = d.pop("Type", UNSET)
        type: Union[Unset, DlnaDlnaProfileType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = DlnaDlnaProfileType(_type)

        dlna_direct_play_profile = cls(
            container=container,
            audio_codec=audio_codec,
            video_codec=video_codec,
            type=type,
        )

        dlna_direct_play_profile.additional_properties = d
        return dlna_direct_play_profile

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
