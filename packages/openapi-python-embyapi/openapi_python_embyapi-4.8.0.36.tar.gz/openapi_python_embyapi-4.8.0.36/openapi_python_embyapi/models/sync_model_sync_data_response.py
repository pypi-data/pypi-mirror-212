from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SyncModelSyncDataResponse")


@attr.s(auto_attribs=True)
class SyncModelSyncDataResponse:
    """
    Attributes:
        item_ids_to_remove (Union[Unset, List[str]]):
    """

    item_ids_to_remove: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        item_ids_to_remove: Union[Unset, List[str]] = UNSET
        if not isinstance(self.item_ids_to_remove, Unset):
            item_ids_to_remove = self.item_ids_to_remove

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if item_ids_to_remove is not UNSET:
            field_dict["ItemIdsToRemove"] = item_ids_to_remove

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        item_ids_to_remove = cast(List[str], d.pop("ItemIdsToRemove", UNSET))

        sync_model_sync_data_response = cls(
            item_ids_to_remove=item_ids_to_remove,
        )

        sync_model_sync_data_response.additional_properties = d
        return sync_model_sync_data_response

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
