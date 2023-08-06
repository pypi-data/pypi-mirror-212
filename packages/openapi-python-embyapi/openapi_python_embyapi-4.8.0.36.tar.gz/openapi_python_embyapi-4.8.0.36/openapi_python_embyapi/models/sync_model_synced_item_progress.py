from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.sync_model_sync_job_item_status import SyncModelSyncJobItemStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="SyncModelSyncedItemProgress")


@attr.s(auto_attribs=True)
class SyncModelSyncedItemProgress:
    """
    Attributes:
        progress (Union[Unset, None, float]):
        status (Union[Unset, SyncModelSyncJobItemStatus]):
    """

    progress: Union[Unset, None, float] = UNSET
    status: Union[Unset, SyncModelSyncJobItemStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        progress = self.progress
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if progress is not UNSET:
            field_dict["Progress"] = progress
        if status is not UNSET:
            field_dict["Status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        progress = d.pop("Progress", UNSET)

        _status = d.pop("Status", UNSET)
        status: Union[Unset, SyncModelSyncJobItemStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = SyncModelSyncJobItemStatus(_status)

        sync_model_synced_item_progress = cls(
            progress=progress,
            status=status,
        )

        sync_model_synced_item_progress.additional_properties = d
        return sync_model_synced_item_progress

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
