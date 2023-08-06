from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dlna_profile_condition_type import DlnaProfileConditionType
from ..models.dlna_profile_condition_value import DlnaProfileConditionValue
from ..types import UNSET, Unset

T = TypeVar("T", bound="DlnaProfileCondition")


@attr.s(auto_attribs=True)
class DlnaProfileCondition:
    """
    Attributes:
        condition (Union[Unset, DlnaProfileConditionType]):
        property_ (Union[Unset, DlnaProfileConditionValue]):
        value (Union[Unset, str]):
        is_required (Union[Unset, bool]):
    """

    condition: Union[Unset, DlnaProfileConditionType] = UNSET
    property_: Union[Unset, DlnaProfileConditionValue] = UNSET
    value: Union[Unset, str] = UNSET
    is_required: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        condition: Union[Unset, str] = UNSET
        if not isinstance(self.condition, Unset):
            condition = self.condition.value

        property_: Union[Unset, str] = UNSET
        if not isinstance(self.property_, Unset):
            property_ = self.property_.value

        value = self.value
        is_required = self.is_required

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if condition is not UNSET:
            field_dict["Condition"] = condition
        if property_ is not UNSET:
            field_dict["Property"] = property_
        if value is not UNSET:
            field_dict["Value"] = value
        if is_required is not UNSET:
            field_dict["IsRequired"] = is_required

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _condition = d.pop("Condition", UNSET)
        condition: Union[Unset, DlnaProfileConditionType]
        if isinstance(_condition, Unset):
            condition = UNSET
        else:
            condition = DlnaProfileConditionType(_condition)

        _property_ = d.pop("Property", UNSET)
        property_: Union[Unset, DlnaProfileConditionValue]
        if isinstance(_property_, Unset):
            property_ = UNSET
        else:
            property_ = DlnaProfileConditionValue(_property_)

        value = d.pop("Value", UNSET)

        is_required = d.pop("IsRequired", UNSET)

        dlna_profile_condition = cls(
            condition=condition,
            property_=property_,
            value=value,
            is_required=is_required,
        )

        dlna_profile_condition.additional_properties = d
        return dlna_profile_condition

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
