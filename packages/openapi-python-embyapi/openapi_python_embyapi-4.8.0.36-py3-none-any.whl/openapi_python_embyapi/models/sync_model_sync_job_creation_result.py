from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sync_model_sync_job_item import SyncModelSyncJobItem
    from ..models.sync_sync_job import SyncSyncJob


T = TypeVar("T", bound="SyncModelSyncJobCreationResult")


@attr.s(auto_attribs=True)
class SyncModelSyncJobCreationResult:
    """
    Attributes:
        job (Union[Unset, SyncSyncJob]):
        job_items (Union[Unset, List['SyncModelSyncJobItem']]):
    """

    job: Union[Unset, "SyncSyncJob"] = UNSET
    job_items: Union[Unset, List["SyncModelSyncJobItem"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.job, Unset):
            job = self.job.to_dict()

        job_items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.job_items, Unset):
            job_items = []
            for job_items_item_data in self.job_items:
                job_items_item = job_items_item_data.to_dict()

                job_items.append(job_items_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job is not UNSET:
            field_dict["Job"] = job
        if job_items is not UNSET:
            field_dict["JobItems"] = job_items

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sync_model_sync_job_item import SyncModelSyncJobItem
        from ..models.sync_sync_job import SyncSyncJob

        d = src_dict.copy()
        _job = d.pop("Job", UNSET)
        job: Union[Unset, SyncSyncJob]
        if isinstance(_job, Unset):
            job = UNSET
        else:
            job = SyncSyncJob.from_dict(_job)

        job_items = []
        _job_items = d.pop("JobItems", UNSET)
        for job_items_item_data in _job_items or []:
            job_items_item = SyncModelSyncJobItem.from_dict(job_items_item_data)

            job_items.append(job_items_item)

        sync_model_sync_job_creation_result = cls(
            job=job,
            job_items=job_items,
        )

        sync_model_sync_job_creation_result.additional_properties = d
        return sync_model_sync_job_creation_result

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
