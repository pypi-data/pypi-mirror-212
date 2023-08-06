from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SyncModelSyncDataRequest")


@attr.s(auto_attribs=True)
class SyncModelSyncDataRequest:
    """
    Attributes:
        local_item_ids (Union[Unset, List[str]]):
        target_id (Union[Unset, str]):
    """

    local_item_ids: Union[Unset, List[str]] = UNSET
    target_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        local_item_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.local_item_ids, Unset):
            local_item_ids = self.local_item_ids

        target_id = self.target_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if local_item_ids is not UNSET:
            field_dict["LocalItemIds"] = local_item_ids
        if target_id is not UNSET:
            field_dict["TargetId"] = target_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        local_item_ids = cast(List[str], d.pop("LocalItemIds", UNSET))

        target_id = d.pop("TargetId", UNSET)

        sync_model_sync_data_request = cls(
            local_item_ids=local_item_ids,
            target_id=target_id,
        )

        sync_model_sync_data_request.additional_properties = d
        return sync_model_sync_data_request

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
