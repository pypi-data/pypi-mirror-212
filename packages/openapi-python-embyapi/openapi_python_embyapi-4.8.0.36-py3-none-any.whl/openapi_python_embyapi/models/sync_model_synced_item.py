import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_item_dto import BaseItemDto
    from ..models.sync_model_item_file_info import SyncModelItemFileInfo


T = TypeVar("T", bound="SyncModelSyncedItem")


@attr.s(auto_attribs=True)
class SyncModelSyncedItem:
    """
    Attributes:
        server_id (Union[Unset, str]):
        sync_job_id (Union[Unset, int]):
        sync_job_name (Union[Unset, str]):
        sync_job_date_created (Union[Unset, datetime.datetime]):
        sync_job_item_id (Union[Unset, int]):
        original_file_name (Union[Unset, str]):
        item (Union[Unset, BaseItemDto]):
        user_id (Union[Unset, str]):
        additional_files (Union[Unset, List['SyncModelItemFileInfo']]):
    """

    server_id: Union[Unset, str] = UNSET
    sync_job_id: Union[Unset, int] = UNSET
    sync_job_name: Union[Unset, str] = UNSET
    sync_job_date_created: Union[Unset, datetime.datetime] = UNSET
    sync_job_item_id: Union[Unset, int] = UNSET
    original_file_name: Union[Unset, str] = UNSET
    item: Union[Unset, "BaseItemDto"] = UNSET
    user_id: Union[Unset, str] = UNSET
    additional_files: Union[Unset, List["SyncModelItemFileInfo"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        server_id = self.server_id
        sync_job_id = self.sync_job_id
        sync_job_name = self.sync_job_name
        sync_job_date_created: Union[Unset, str] = UNSET
        if not isinstance(self.sync_job_date_created, Unset):
            sync_job_date_created = self.sync_job_date_created.isoformat()

        sync_job_item_id = self.sync_job_item_id
        original_file_name = self.original_file_name
        item: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.item, Unset):
            item = self.item.to_dict()

        user_id = self.user_id
        additional_files: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.additional_files, Unset):
            additional_files = []
            for additional_files_item_data in self.additional_files:
                additional_files_item = additional_files_item_data.to_dict()

                additional_files.append(additional_files_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if server_id is not UNSET:
            field_dict["ServerId"] = server_id
        if sync_job_id is not UNSET:
            field_dict["SyncJobId"] = sync_job_id
        if sync_job_name is not UNSET:
            field_dict["SyncJobName"] = sync_job_name
        if sync_job_date_created is not UNSET:
            field_dict["SyncJobDateCreated"] = sync_job_date_created
        if sync_job_item_id is not UNSET:
            field_dict["SyncJobItemId"] = sync_job_item_id
        if original_file_name is not UNSET:
            field_dict["OriginalFileName"] = original_file_name
        if item is not UNSET:
            field_dict["Item"] = item
        if user_id is not UNSET:
            field_dict["UserId"] = user_id
        if additional_files is not UNSET:
            field_dict["AdditionalFiles"] = additional_files

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.base_item_dto import BaseItemDto
        from ..models.sync_model_item_file_info import SyncModelItemFileInfo

        d = src_dict.copy()
        server_id = d.pop("ServerId", UNSET)

        sync_job_id = d.pop("SyncJobId", UNSET)

        sync_job_name = d.pop("SyncJobName", UNSET)

        _sync_job_date_created = d.pop("SyncJobDateCreated", UNSET)
        sync_job_date_created: Union[Unset, datetime.datetime]
        if isinstance(_sync_job_date_created, Unset):
            sync_job_date_created = UNSET
        else:
            sync_job_date_created = isoparse(_sync_job_date_created)

        sync_job_item_id = d.pop("SyncJobItemId", UNSET)

        original_file_name = d.pop("OriginalFileName", UNSET)

        _item = d.pop("Item", UNSET)
        item: Union[Unset, BaseItemDto]
        if isinstance(_item, Unset):
            item = UNSET
        else:
            item = BaseItemDto.from_dict(_item)

        user_id = d.pop("UserId", UNSET)

        additional_files = []
        _additional_files = d.pop("AdditionalFiles", UNSET)
        for additional_files_item_data in _additional_files or []:
            additional_files_item = SyncModelItemFileInfo.from_dict(additional_files_item_data)

            additional_files.append(additional_files_item)

        sync_model_synced_item = cls(
            server_id=server_id,
            sync_job_id=sync_job_id,
            sync_job_name=sync_job_name,
            sync_job_date_created=sync_job_date_created,
            sync_job_item_id=sync_job_item_id,
            original_file_name=original_file_name,
            item=item,
            user_id=user_id,
            additional_files=additional_files,
        )

        sync_model_synced_item.additional_properties = d
        return sync_model_synced_item

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
