import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.sync_sync_category import SyncSyncCategory
from ..models.sync_sync_job_status import SyncSyncJobStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="SyncSyncJob")


@attr.s(auto_attribs=True)
class SyncSyncJob:
    """
    Attributes:
        id (Union[Unset, int]):
        target_id (Union[Unset, str]):
        target_name (Union[Unset, str]):
        quality (Union[Unset, str]):
        bitrate (Union[Unset, None, int]):
        container (Union[Unset, str]):
        video_codec (Union[Unset, str]):
        audio_codec (Union[Unset, str]):
        profile (Union[Unset, str]):
        category (Union[Unset, SyncSyncCategory]):
        parent_id (Union[Unset, int]):
        progress (Union[Unset, float]):
        name (Union[Unset, str]):
        status (Union[Unset, SyncSyncJobStatus]):
        user_id (Union[Unset, int]):
        unwatched_only (Union[Unset, bool]):
        sync_new_content (Union[Unset, bool]):
        item_limit (Union[Unset, None, int]):
        requested_item_ids (Union[Unset, List[int]]):
        date_created (Union[Unset, datetime.datetime]):
        date_last_modified (Union[Unset, datetime.datetime]):
        item_count (Union[Unset, int]):
        parent_name (Union[Unset, str]):
        primary_image_item_id (Union[Unset, str]):
        primary_image_tag (Union[Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    target_id: Union[Unset, str] = UNSET
    target_name: Union[Unset, str] = UNSET
    quality: Union[Unset, str] = UNSET
    bitrate: Union[Unset, None, int] = UNSET
    container: Union[Unset, str] = UNSET
    video_codec: Union[Unset, str] = UNSET
    audio_codec: Union[Unset, str] = UNSET
    profile: Union[Unset, str] = UNSET
    category: Union[Unset, SyncSyncCategory] = UNSET
    parent_id: Union[Unset, int] = UNSET
    progress: Union[Unset, float] = UNSET
    name: Union[Unset, str] = UNSET
    status: Union[Unset, SyncSyncJobStatus] = UNSET
    user_id: Union[Unset, int] = UNSET
    unwatched_only: Union[Unset, bool] = UNSET
    sync_new_content: Union[Unset, bool] = UNSET
    item_limit: Union[Unset, None, int] = UNSET
    requested_item_ids: Union[Unset, List[int]] = UNSET
    date_created: Union[Unset, datetime.datetime] = UNSET
    date_last_modified: Union[Unset, datetime.datetime] = UNSET
    item_count: Union[Unset, int] = UNSET
    parent_name: Union[Unset, str] = UNSET
    primary_image_item_id: Union[Unset, str] = UNSET
    primary_image_tag: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        target_id = self.target_id
        target_name = self.target_name
        quality = self.quality
        bitrate = self.bitrate
        container = self.container
        video_codec = self.video_codec
        audio_codec = self.audio_codec
        profile = self.profile
        category: Union[Unset, str] = UNSET
        if not isinstance(self.category, Unset):
            category = self.category.value

        parent_id = self.parent_id
        progress = self.progress
        name = self.name
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        user_id = self.user_id
        unwatched_only = self.unwatched_only
        sync_new_content = self.sync_new_content
        item_limit = self.item_limit
        requested_item_ids: Union[Unset, List[int]] = UNSET
        if not isinstance(self.requested_item_ids, Unset):
            requested_item_ids = self.requested_item_ids

        date_created: Union[Unset, str] = UNSET
        if not isinstance(self.date_created, Unset):
            date_created = self.date_created.isoformat()

        date_last_modified: Union[Unset, str] = UNSET
        if not isinstance(self.date_last_modified, Unset):
            date_last_modified = self.date_last_modified.isoformat()

        item_count = self.item_count
        parent_name = self.parent_name
        primary_image_item_id = self.primary_image_item_id
        primary_image_tag = self.primary_image_tag

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if target_id is not UNSET:
            field_dict["TargetId"] = target_id
        if target_name is not UNSET:
            field_dict["TargetName"] = target_name
        if quality is not UNSET:
            field_dict["Quality"] = quality
        if bitrate is not UNSET:
            field_dict["Bitrate"] = bitrate
        if container is not UNSET:
            field_dict["Container"] = container
        if video_codec is not UNSET:
            field_dict["VideoCodec"] = video_codec
        if audio_codec is not UNSET:
            field_dict["AudioCodec"] = audio_codec
        if profile is not UNSET:
            field_dict["Profile"] = profile
        if category is not UNSET:
            field_dict["Category"] = category
        if parent_id is not UNSET:
            field_dict["ParentId"] = parent_id
        if progress is not UNSET:
            field_dict["Progress"] = progress
        if name is not UNSET:
            field_dict["Name"] = name
        if status is not UNSET:
            field_dict["Status"] = status
        if user_id is not UNSET:
            field_dict["UserId"] = user_id
        if unwatched_only is not UNSET:
            field_dict["UnwatchedOnly"] = unwatched_only
        if sync_new_content is not UNSET:
            field_dict["SyncNewContent"] = sync_new_content
        if item_limit is not UNSET:
            field_dict["ItemLimit"] = item_limit
        if requested_item_ids is not UNSET:
            field_dict["RequestedItemIds"] = requested_item_ids
        if date_created is not UNSET:
            field_dict["DateCreated"] = date_created
        if date_last_modified is not UNSET:
            field_dict["DateLastModified"] = date_last_modified
        if item_count is not UNSET:
            field_dict["ItemCount"] = item_count
        if parent_name is not UNSET:
            field_dict["ParentName"] = parent_name
        if primary_image_item_id is not UNSET:
            field_dict["PrimaryImageItemId"] = primary_image_item_id
        if primary_image_tag is not UNSET:
            field_dict["PrimaryImageTag"] = primary_image_tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        target_id = d.pop("TargetId", UNSET)

        target_name = d.pop("TargetName", UNSET)

        quality = d.pop("Quality", UNSET)

        bitrate = d.pop("Bitrate", UNSET)

        container = d.pop("Container", UNSET)

        video_codec = d.pop("VideoCodec", UNSET)

        audio_codec = d.pop("AudioCodec", UNSET)

        profile = d.pop("Profile", UNSET)

        _category = d.pop("Category", UNSET)
        category: Union[Unset, SyncSyncCategory]
        if isinstance(_category, Unset):
            category = UNSET
        else:
            category = SyncSyncCategory(_category)

        parent_id = d.pop("ParentId", UNSET)

        progress = d.pop("Progress", UNSET)

        name = d.pop("Name", UNSET)

        _status = d.pop("Status", UNSET)
        status: Union[Unset, SyncSyncJobStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = SyncSyncJobStatus(_status)

        user_id = d.pop("UserId", UNSET)

        unwatched_only = d.pop("UnwatchedOnly", UNSET)

        sync_new_content = d.pop("SyncNewContent", UNSET)

        item_limit = d.pop("ItemLimit", UNSET)

        requested_item_ids = cast(List[int], d.pop("RequestedItemIds", UNSET))

        _date_created = d.pop("DateCreated", UNSET)
        date_created: Union[Unset, datetime.datetime]
        if isinstance(_date_created, Unset):
            date_created = UNSET
        else:
            date_created = isoparse(_date_created)

        _date_last_modified = d.pop("DateLastModified", UNSET)
        date_last_modified: Union[Unset, datetime.datetime]
        if isinstance(_date_last_modified, Unset):
            date_last_modified = UNSET
        else:
            date_last_modified = isoparse(_date_last_modified)

        item_count = d.pop("ItemCount", UNSET)

        parent_name = d.pop("ParentName", UNSET)

        primary_image_item_id = d.pop("PrimaryImageItemId", UNSET)

        primary_image_tag = d.pop("PrimaryImageTag", UNSET)

        sync_sync_job = cls(
            id=id,
            target_id=target_id,
            target_name=target_name,
            quality=quality,
            bitrate=bitrate,
            container=container,
            video_codec=video_codec,
            audio_codec=audio_codec,
            profile=profile,
            category=category,
            parent_id=parent_id,
            progress=progress,
            name=name,
            status=status,
            user_id=user_id,
            unwatched_only=unwatched_only,
            sync_new_content=sync_new_content,
            item_limit=item_limit,
            requested_item_ids=requested_item_ids,
            date_created=date_created,
            date_last_modified=date_last_modified,
            item_count=item_count,
            parent_name=parent_name,
            primary_image_item_id=primary_image_item_id,
            primary_image_tag=primary_image_tag,
        )

        sync_sync_job.additional_properties = d
        return sync_sync_job

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
