from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dlna_dlna_profile_type import DlnaDlnaProfileType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dlna_profile_condition import DlnaProfileCondition


T = TypeVar("T", bound="DlnaResponseProfile")


@attr.s(auto_attribs=True)
class DlnaResponseProfile:
    """
    Attributes:
        container (Union[Unset, str]):
        audio_codec (Union[Unset, str]):
        video_codec (Union[Unset, str]):
        type (Union[Unset, DlnaDlnaProfileType]):
        org_pn (Union[Unset, str]):
        mime_type (Union[Unset, str]):
        conditions (Union[Unset, List['DlnaProfileCondition']]):
    """

    container: Union[Unset, str] = UNSET
    audio_codec: Union[Unset, str] = UNSET
    video_codec: Union[Unset, str] = UNSET
    type: Union[Unset, DlnaDlnaProfileType] = UNSET
    org_pn: Union[Unset, str] = UNSET
    mime_type: Union[Unset, str] = UNSET
    conditions: Union[Unset, List["DlnaProfileCondition"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        container = self.container
        audio_codec = self.audio_codec
        video_codec = self.video_codec
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        org_pn = self.org_pn
        mime_type = self.mime_type
        conditions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.conditions, Unset):
            conditions = []
            for conditions_item_data in self.conditions:
                conditions_item = conditions_item_data.to_dict()

                conditions.append(conditions_item)

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
        if org_pn is not UNSET:
            field_dict["OrgPn"] = org_pn
        if mime_type is not UNSET:
            field_dict["MimeType"] = mime_type
        if conditions is not UNSET:
            field_dict["Conditions"] = conditions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dlna_profile_condition import DlnaProfileCondition

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

        org_pn = d.pop("OrgPn", UNSET)

        mime_type = d.pop("MimeType", UNSET)

        conditions = []
        _conditions = d.pop("Conditions", UNSET)
        for conditions_item_data in _conditions or []:
            conditions_item = DlnaProfileCondition.from_dict(conditions_item_data)

            conditions.append(conditions_item)

        dlna_response_profile = cls(
            container=container,
            audio_codec=audio_codec,
            video_codec=video_codec,
            type=type,
            org_pn=org_pn,
            mime_type=mime_type,
            conditions=conditions,
        )

        dlna_response_profile.additional_properties = d
        return dlna_response_profile

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
