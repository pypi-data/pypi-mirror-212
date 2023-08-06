from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.attributes_simple_condition import AttributesSimpleCondition
from ..models.attributes_value_condition import AttributesValueCondition
from ..models.emby_web_generic_edit_conditions_property_condition_type import (
    EmbyWebGenericEditConditionsPropertyConditionType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.emby_web_generic_edit_conditions_property_condition_value import (
        EmbyWebGenericEditConditionsPropertyConditionValue,
    )


T = TypeVar("T", bound="EmbyWebGenericEditConditionsPropertyCondition")


@attr.s(auto_attribs=True)
class EmbyWebGenericEditConditionsPropertyCondition:
    """
    Attributes:
        affected_property_id (Union[Unset, str]):
        condition_type (Union[Unset, EmbyWebGenericEditConditionsPropertyConditionType]):
        target_property_id (Union[Unset, str]):
        simple_condition (Union[Unset, AttributesSimpleCondition]):
        value_condition (Union[Unset, AttributesValueCondition]):
        value (Union[Unset, EmbyWebGenericEditConditionsPropertyConditionValue]):
    """

    affected_property_id: Union[Unset, str] = UNSET
    condition_type: Union[Unset, EmbyWebGenericEditConditionsPropertyConditionType] = UNSET
    target_property_id: Union[Unset, str] = UNSET
    simple_condition: Union[Unset, AttributesSimpleCondition] = UNSET
    value_condition: Union[Unset, AttributesValueCondition] = UNSET
    value: Union[Unset, "EmbyWebGenericEditConditionsPropertyConditionValue"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        affected_property_id = self.affected_property_id
        condition_type: Union[Unset, str] = UNSET
        if not isinstance(self.condition_type, Unset):
            condition_type = self.condition_type.value

        target_property_id = self.target_property_id
        simple_condition: Union[Unset, str] = UNSET
        if not isinstance(self.simple_condition, Unset):
            simple_condition = self.simple_condition.value

        value_condition: Union[Unset, str] = UNSET
        if not isinstance(self.value_condition, Unset):
            value_condition = self.value_condition.value

        value: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.value, Unset):
            value = self.value.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if affected_property_id is not UNSET:
            field_dict["AffectedPropertyId"] = affected_property_id
        if condition_type is not UNSET:
            field_dict["ConditionType"] = condition_type
        if target_property_id is not UNSET:
            field_dict["TargetPropertyId"] = target_property_id
        if simple_condition is not UNSET:
            field_dict["SimpleCondition"] = simple_condition
        if value_condition is not UNSET:
            field_dict["ValueCondition"] = value_condition
        if value is not UNSET:
            field_dict["Value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.emby_web_generic_edit_conditions_property_condition_value import (
            EmbyWebGenericEditConditionsPropertyConditionValue,
        )

        d = src_dict.copy()
        affected_property_id = d.pop("AffectedPropertyId", UNSET)

        _condition_type = d.pop("ConditionType", UNSET)
        condition_type: Union[Unset, EmbyWebGenericEditConditionsPropertyConditionType]
        if isinstance(_condition_type, Unset):
            condition_type = UNSET
        else:
            condition_type = EmbyWebGenericEditConditionsPropertyConditionType(_condition_type)

        target_property_id = d.pop("TargetPropertyId", UNSET)

        _simple_condition = d.pop("SimpleCondition", UNSET)
        simple_condition: Union[Unset, AttributesSimpleCondition]
        if isinstance(_simple_condition, Unset):
            simple_condition = UNSET
        else:
            simple_condition = AttributesSimpleCondition(_simple_condition)

        _value_condition = d.pop("ValueCondition", UNSET)
        value_condition: Union[Unset, AttributesValueCondition]
        if isinstance(_value_condition, Unset):
            value_condition = UNSET
        else:
            value_condition = AttributesValueCondition(_value_condition)

        _value = d.pop("Value", UNSET)
        value: Union[Unset, EmbyWebGenericEditConditionsPropertyConditionValue]
        if isinstance(_value, Unset):
            value = UNSET
        else:
            value = EmbyWebGenericEditConditionsPropertyConditionValue.from_dict(_value)

        emby_web_generic_edit_conditions_property_condition = cls(
            affected_property_id=affected_property_id,
            condition_type=condition_type,
            target_property_id=target_property_id,
            simple_condition=simple_condition,
            value_condition=value_condition,
            value=value,
        )

        emby_web_generic_edit_conditions_property_condition.additional_properties = d
        return emby_web_generic_edit_conditions_property_condition

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
