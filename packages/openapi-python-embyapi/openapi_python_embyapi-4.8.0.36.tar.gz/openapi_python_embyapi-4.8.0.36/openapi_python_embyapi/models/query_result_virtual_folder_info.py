from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.virtual_folder_info import VirtualFolderInfo


T = TypeVar("T", bound="QueryResultVirtualFolderInfo")


@attr.s(auto_attribs=True)
class QueryResultVirtualFolderInfo:
    """
    Attributes:
        items (Union[Unset, List['VirtualFolderInfo']]):
        total_record_count (Union[Unset, int]):
    """

    items: Union[Unset, List["VirtualFolderInfo"]] = UNSET
    total_record_count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()

                items.append(items_item)

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
        from ..models.virtual_folder_info import VirtualFolderInfo

        d = src_dict.copy()
        items = []
        _items = d.pop("Items", UNSET)
        for items_item_data in _items or []:
            items_item = VirtualFolderInfo.from_dict(items_item_data)

            items.append(items_item)

        total_record_count = d.pop("TotalRecordCount", UNSET)

        query_result_virtual_folder_info = cls(
            items=items,
            total_record_count=total_record_count,
        )

        query_result_virtual_folder_info.additional_properties = d
        return query_result_virtual_folder_info

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
