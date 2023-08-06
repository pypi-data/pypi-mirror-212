from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TupleDoubleDouble")


@attr.s(auto_attribs=True)
class TupleDoubleDouble:
    """
    Attributes:
        item_1 (Union[Unset, float]):
        item_2 (Union[Unset, float]):
    """

    item_1: Union[Unset, float] = UNSET
    item_2: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        item_1 = self.item_1
        item_2 = self.item_2

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if item_1 is not UNSET:
            field_dict["Item1"] = item_1
        if item_2 is not UNSET:
            field_dict["Item2"] = item_2

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        item_1 = d.pop("Item1", UNSET)

        item_2 = d.pop("Item2", UNSET)

        tuple_double_double = cls(
            item_1=item_1,
            item_2=item_2,
        )

        tuple_double_double.additional_properties = d
        return tuple_double_double

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
