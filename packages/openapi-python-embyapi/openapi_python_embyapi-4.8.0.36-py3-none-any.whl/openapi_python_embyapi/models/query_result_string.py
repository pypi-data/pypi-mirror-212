from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="QueryResultString")


@attr.s(auto_attribs=True)
class QueryResultString:
    """
    Attributes:
        items (Union[Unset, List[str]]):
        total_record_count (Union[Unset, int]):
    """

    items: Union[Unset, List[str]] = UNSET
    total_record_count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        items: Union[Unset, List[str]] = UNSET
        if not isinstance(self.items, Unset):
            items = self.items

        total_record_count = self.total_record_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if items is not UNSET:
            field_dict["Items"] = items
        if total_record_count is not UNSET:
            field_dict["TotalRecordCount"] = total_record_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        items = cast(List[str], d.pop("Items", UNSET))

        total_record_count = d.pop("TotalRecordCount", UNSET)

        query_result_string = cls(
            items=items,
            total_record_count=total_record_count,
        )

        query_result_string.additional_properties = d
        return query_result_string

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
