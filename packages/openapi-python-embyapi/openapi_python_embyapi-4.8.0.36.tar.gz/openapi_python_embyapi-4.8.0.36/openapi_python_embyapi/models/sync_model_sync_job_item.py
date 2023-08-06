import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.sync_model_sync_job_item_status import SyncModelSyncJobItemStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.media_source_info import MediaSourceInfo
    from ..models.sync_model_item_file_info import SyncModelItemFileInfo


T = TypeVar("T", bound="SyncModelSyncJobItem")


@attr.s(auto_attribs=True)
class SyncModelSyncJobItem:
    """
    Attributes:
        id (Union[Unset, int]):
        job_id (Union[Unset, int]):
        item_id (Union[Unset, int]):
        item_name (Union[Unset, str]):
        media_source_id (Union[Unset, str]):
        media_source (Union[Unset, MediaSourceInfo]):
        target_id (Union[Unset, str]):
        output_path (Union[Unset, str]):
        status (Union[Unset, SyncModelSyncJobItemStatus]):
        progress (Union[Unset, None, float]):
        date_created (Union[Unset, datetime.datetime]):
        primary_image_item_id (Union[Unset, str]):
        primary_image_tag (Union[Unset, str]):
        temporary_path (Union[Unset, str]):
        additional_files (Union[Unset, List['SyncModelItemFileInfo']]):
    """

    id: Union[Unset, int] = UNSET
    job_id: Union[Unset, int] = UNSET
    item_id: Union[Unset, int] = UNSET
    item_name: Union[Unset, str] = UNSET
    media_source_id: Union[Unset, str] = UNSET
    media_source: Union[Unset, "MediaSourceInfo"] = UNSET
    target_id: Union[Unset, str] = UNSET
    output_path: Union[Unset, str] = UNSET
    status: Union[Unset, SyncModelSyncJobItemStatus] = UNSET
    progress: Union[Unset, None, float] = UNSET
    date_created: Union[Unset, datetime.datetime] = UNSET
    primary_image_item_id: Union[Unset, str] = UNSET
    primary_image_tag: Union[Unset, str] = UNSET
    temporary_path: Union[Unset, str] = UNSET
    additional_files: Union[Unset, List["SyncModelItemFileInfo"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        job_id = self.job_id
        item_id = self.item_id
        item_name = self.item_name
        media_source_id = self.media_source_id
        media_source: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.media_source, Unset):
            media_source = self.media_source.to_dict()

        target_id = self.target_id
        output_path = self.output_path
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        progress = self.progress
        date_created: Union[Unset, str] = UNSET
        if not isinstance(self.date_created, Unset):
            date_created = self.date_created.isoformat()

        primary_image_item_id = self.primary_image_item_id
        primary_image_tag = self.primary_image_tag
        temporary_path = self.temporary_path
        additional_files: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.additional_files, Unset):
            additional_files = []
            for additional_files_item_data in self.additional_files:
                additional_files_item = additional_files_item_data.to_dict()

                additional_files.append(additional_files_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if job_id is not UNSET:
            field_dict["JobId"] = job_id
        if item_id is not UNSET:
            field_dict["ItemId"] = item_id
        if item_name is not UNSET:
            field_dict["ItemName"] = item_name
        if media_source_id is not UNSET:
            field_dict["MediaSourceId"] = media_source_id
        if media_source is not UNSET:
            field_dict["MediaSource"] = media_source
        if target_id is not UNSET:
            field_dict["TargetId"] = target_id
        if output_path is not UNSET:
            field_dict["OutputPath"] = output_path
        if status is not UNSET:
            field_dict["Status"] = status
        if progress is not UNSET:
            field_dict["Progress"] = progress
        if date_created is not UNSET:
            field_dict["DateCreated"] = date_created
        if primary_image_item_id is not UNSET:
            field_dict["PrimaryImageItemId"] = primary_image_item_id
        if primary_image_tag is not UNSET:
            field_dict["PrimaryImageTag"] = primary_image_tag
        if temporary_path is not UNSET:
            field_dict["TemporaryPath"] = temporary_path
        if additional_files is not UNSET:
            field_dict["AdditionalFiles"] = additional_files

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.media_source_info import MediaSourceInfo
        from ..models.sync_model_item_file_info import SyncModelItemFileInfo

        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        job_id = d.pop("JobId", UNSET)

        item_id = d.pop("ItemId", UNSET)

        item_name = d.pop("ItemName", UNSET)

        media_source_id = d.pop("MediaSourceId", UNSET)

        _media_source = d.pop("MediaSource", UNSET)
        media_source: Union[Unset, MediaSourceInfo]
        if isinstance(_media_source, Unset):
            media_source = UNSET
        else:
            media_source = MediaSourceInfo.from_dict(_media_source)

        target_id = d.pop("TargetId", UNSET)

        output_path = d.pop("OutputPath", UNSET)

        _status = d.pop("Status", UNSET)
        status: Union[Unset, SyncModelSyncJobItemStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = SyncModelSyncJobItemStatus(_status)

        progress = d.pop("Progress", UNSET)

        _date_created = d.pop("DateCreated", UNSET)
        date_created: Union[Unset, datetime.datetime]
        if isinstance(_date_created, Unset):
            date_created = UNSET
        else:
            date_created = isoparse(_date_created)

        primary_image_item_id = d.pop("PrimaryImageItemId", UNSET)

        primary_image_tag = d.pop("PrimaryImageTag", UNSET)

        temporary_path = d.pop("TemporaryPath", UNSET)

        additional_files = []
        _additional_files = d.pop("AdditionalFiles", UNSET)
        for additional_files_item_data in _additional_files or []:
            additional_files_item = SyncModelItemFileInfo.from_dict(additional_files_item_data)

            additional_files.append(additional_files_item)

        sync_model_sync_job_item = cls(
            id=id,
            job_id=job_id,
            item_id=item_id,
            item_name=item_name,
            media_source_id=media_source_id,
            media_source=media_source,
            target_id=target_id,
            output_path=output_path,
            status=status,
            progress=progress,
            date_created=date_created,
            primary_image_item_id=primary_image_item_id,
            primary_image_tag=primary_image_tag,
            temporary_path=temporary_path,
            additional_files=additional_files,
        )

        sync_model_sync_job_item.additional_properties = d
        return sync_model_sync_job_item

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
