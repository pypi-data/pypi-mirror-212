from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dlna_codec_type import DlnaCodecType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dlna_profile_condition import DlnaProfileCondition


T = TypeVar("T", bound="DlnaCodecProfile")


@attr.s(auto_attribs=True)
class DlnaCodecProfile:
    """
    Attributes:
        type (Union[Unset, DlnaCodecType]):
        conditions (Union[Unset, List['DlnaProfileCondition']]):
        apply_conditions (Union[Unset, List['DlnaProfileCondition']]):
        codec (Union[Unset, str]):
        container (Union[Unset, str]):
    """

    type: Union[Unset, DlnaCodecType] = UNSET
    conditions: Union[Unset, List["DlnaProfileCondition"]] = UNSET
    apply_conditions: Union[Unset, List["DlnaProfileCondition"]] = UNSET
    codec: Union[Unset, str] = UNSET
    container: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        conditions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.conditions, Unset):
            conditions = []
            for conditions_item_data in self.conditions:
                conditions_item = conditions_item_data.to_dict()

                conditions.append(conditions_item)

        apply_conditions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.apply_conditions, Unset):
            apply_conditions = []
            for apply_conditions_item_data in self.apply_conditions:
                apply_conditions_item = apply_conditions_item_data.to_dict()

                apply_conditions.append(apply_conditions_item)

        codec = self.codec
        container = self.container

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["Type"] = type
        if conditions is not UNSET:
            field_dict["Conditions"] = conditions
        if apply_conditions is not UNSET:
            field_dict["ApplyConditions"] = apply_conditions
        if codec is not UNSET:
            field_dict["Codec"] = codec
        if container is not UNSET:
            field_dict["Container"] = container

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dlna_profile_condition import DlnaProfileCondition

        d = src_dict.copy()
        _type = d.pop("Type", UNSET)
        type: Union[Unset, DlnaCodecType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = DlnaCodecType(_type)

        conditions = []
        _conditions = d.pop("Conditions", UNSET)
        for conditions_item_data in _conditions or []:
            conditions_item = DlnaProfileCondition.from_dict(conditions_item_data)

            conditions.append(conditions_item)

        apply_conditions = []
        _apply_conditions = d.pop("ApplyConditions", UNSET)
        for apply_conditions_item_data in _apply_conditions or []:
            apply_conditions_item = DlnaProfileCondition.from_dict(apply_conditions_item_data)

            apply_conditions.append(apply_conditions_item)

        codec = d.pop("Codec", UNSET)

        container = d.pop("Container", UNSET)

        dlna_codec_profile = cls(
            type=type,
            conditions=conditions,
            apply_conditions=apply_conditions,
            codec=codec,
            container=container,
        )

        dlna_codec_profile.additional_properties = d
        return dlna_codec_profile

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
