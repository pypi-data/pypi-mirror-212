from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.sync_sync_category import SyncSyncCategory
from ..types import UNSET, Unset

T = TypeVar("T", bound="SyncModelSyncJobRequest")


@attr.s(auto_attribs=True)
class SyncModelSyncJobRequest:
    """
    Attributes:
        target_id (Union[Unset, str]):
        item_ids (Union[Unset, List[str]]):
        category (Union[Unset, SyncSyncCategory]):
        parent_id (Union[Unset, str]):
        quality (Union[Unset, str]):
        profile (Union[Unset, str]):
        container (Union[Unset, str]):
        video_codec (Union[Unset, str]):
        audio_codec (Union[Unset, str]):
        name (Union[Unset, str]):
        user_id (Union[Unset, str]):
        unwatched_only (Union[Unset, bool]):
        sync_new_content (Union[Unset, bool]):
        item_limit (Union[Unset, None, int]):
        bitrate (Union[Unset, None, int]):
        downloaded (Union[Unset, bool]):
    """

    target_id: Union[Unset, str] = UNSET
    item_ids: Union[Unset, List[str]] = UNSET
    category: Union[Unset, SyncSyncCategory] = UNSET
    parent_id: Union[Unset, str] = UNSET
    quality: Union[Unset, str] = UNSET
    profile: Union[Unset, str] = UNSET
    container: Union[Unset, str] = UNSET
    video_codec: Union[Unset, str] = UNSET
    audio_codec: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    user_id: Union[Unset, str] = UNSET
    unwatched_only: Union[Unset, bool] = UNSET
    sync_new_content: Union[Unset, bool] = UNSET
    item_limit: Union[Unset, None, int] = UNSET
    bitrate: Union[Unset, None, int] = UNSET
    downloaded: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        target_id = self.target_id
        item_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.item_ids, Unset):
            item_ids = self.item_ids

        category: Union[Unset, str] = UNSET
        if not isinstance(self.category, Unset):
            category = self.category.value

        parent_id = self.parent_id
        quality = self.quality
        profile = self.profile
        container = self.container
        video_codec = self.video_codec
        audio_codec = self.audio_codec
        name = self.name
        user_id = self.user_id
        unwatched_only = self.unwatched_only
        sync_new_content = self.sync_new_content
        item_limit = self.item_limit
        bitrate = self.bitrate
        downloaded = self.downloaded

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if target_id is not UNSET:
            field_dict["TargetId"] = target_id
        if item_ids is not UNSET:
            field_dict["ItemIds"] = item_ids
        if category is not UNSET:
            field_dict["Category"] = category
        if parent_id is not UNSET:
            field_dict["ParentId"] = parent_id
        if quality is not UNSET:
            field_dict["Quality"] = quality
        if profile is not UNSET:
            field_dict["Profile"] = profile
        if container is not UNSET:
            field_dict["Container"] = container
        if video_codec is not UNSET:
            field_dict["VideoCodec"] = video_codec
        if audio_codec is not UNSET:
            field_dict["AudioCodec"] = audio_codec
        if name is not UNSET:
            field_dict["Name"] = name
        if user_id is not UNSET:
            field_dict["UserId"] = user_id
        if unwatched_only is not UNSET:
            field_dict["UnwatchedOnly"] = unwatched_only
        if sync_new_content is not UNSET:
            field_dict["SyncNewContent"] = sync_new_content
        if item_limit is not UNSET:
            field_dict["ItemLimit"] = item_limit
        if bitrate is not UNSET:
            field_dict["Bitrate"] = bitrate
        if downloaded is not UNSET:
            field_dict["Downloaded"] = downloaded

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        target_id = d.pop("TargetId", UNSET)

        item_ids = cast(List[str], d.pop("ItemIds", UNSET))

        _category = d.pop("Category", UNSET)
        category: Union[Unset, SyncSyncCategory]
        if isinstance(_category, Unset):
            category = UNSET
        else:
            category = SyncSyncCategory(_category)

        parent_id = d.pop("ParentId", UNSET)

        quality = d.pop("Quality", UNSET)

        profile = d.pop("Profile", UNSET)

        container = d.pop("Container", UNSET)

        video_codec = d.pop("VideoCodec", UNSET)

        audio_codec = d.pop("AudioCodec", UNSET)

        name = d.pop("Name", UNSET)

        user_id = d.pop("UserId", UNSET)

        unwatched_only = d.pop("UnwatchedOnly", UNSET)

        sync_new_content = d.pop("SyncNewContent", UNSET)

        item_limit = d.pop("ItemLimit", UNSET)

        bitrate = d.pop("Bitrate", UNSET)

        downloaded = d.pop("Downloaded", UNSET)

        sync_model_sync_job_request = cls(
            target_id=target_id,
            item_ids=item_ids,
            category=category,
            parent_id=parent_id,
            quality=quality,
            profile=profile,
            container=container,
            video_codec=video_codec,
            audio_codec=audio_codec,
            name=name,
            user_id=user_id,
            unwatched_only=unwatched_only,
            sync_new_content=sync_new_content,
            item_limit=item_limit,
            bitrate=bitrate,
            downloaded=downloaded,
        )

        sync_model_sync_job_request.additional_properties = d
        return sync_model_sync_job_request

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
