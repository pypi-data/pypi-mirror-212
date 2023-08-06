from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.configuration_unrated_item import ConfigurationUnratedItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.configuration_access_schedule import ConfigurationAccessSchedule


T = TypeVar("T", bound="UsersUserPolicy")


@attr.s(auto_attribs=True)
class UsersUserPolicy:
    """
    Attributes:
        is_administrator (Union[Unset, bool]):
        is_hidden (Union[Unset, bool]):
        is_hidden_remotely (Union[Unset, bool]):
        is_hidden_from_unused_devices (Union[Unset, bool]):
        is_disabled (Union[Unset, bool]):
        max_parental_rating (Union[Unset, None, int]):
        allow_tag_or_rating (Union[Unset, bool]):
        blocked_tags (Union[Unset, List[str]]):
        is_tag_blocking_mode_inclusive (Union[Unset, bool]):
        include_tags (Union[Unset, List[str]]):
        enable_user_preference_access (Union[Unset, bool]):
        access_schedules (Union[Unset, List['ConfigurationAccessSchedule']]):
        block_unrated_items (Union[Unset, List[ConfigurationUnratedItem]]):
        enable_remote_control_of_other_users (Union[Unset, bool]):
        enable_shared_device_control (Union[Unset, bool]):
        enable_remote_access (Union[Unset, bool]):
        enable_live_tv_management (Union[Unset, bool]):
        enable_live_tv_access (Union[Unset, bool]):
        enable_media_playback (Union[Unset, bool]):
        enable_audio_playback_transcoding (Union[Unset, bool]):
        enable_video_playback_transcoding (Union[Unset, bool]):
        enable_playback_remuxing (Union[Unset, bool]):
        enable_content_deletion (Union[Unset, bool]):
        restricted_features (Union[Unset, List[str]]):
        enable_content_deletion_from_folders (Union[Unset, List[str]]):
        enable_content_downloading (Union[Unset, bool]):
        enable_subtitle_downloading (Union[Unset, bool]):
        enable_subtitle_management (Union[Unset, bool]):
        enable_sync_transcoding (Union[Unset, bool]):
        enable_media_conversion (Union[Unset, bool]):
        enabled_channels (Union[Unset, List[str]]):
        enable_all_channels (Union[Unset, bool]):
        enabled_folders (Union[Unset, List[str]]):
        enable_all_folders (Union[Unset, bool]):
        invalid_login_attempt_count (Union[Unset, int]):
        enable_public_sharing (Union[Unset, bool]):
        blocked_media_folders (Union[Unset, List[str]]):
        remote_client_bitrate_limit (Union[Unset, int]):
        authentication_provider_id (Union[Unset, str]):
        excluded_sub_folders (Union[Unset, List[str]]):
        simultaneous_stream_limit (Union[Unset, int]):
        enabled_devices (Union[Unset, List[str]]):
        enable_all_devices (Union[Unset, bool]):
    """

    is_administrator: Union[Unset, bool] = UNSET
    is_hidden: Union[Unset, bool] = UNSET
    is_hidden_remotely: Union[Unset, bool] = UNSET
    is_hidden_from_unused_devices: Union[Unset, bool] = UNSET
    is_disabled: Union[Unset, bool] = UNSET
    max_parental_rating: Union[Unset, None, int] = UNSET
    allow_tag_or_rating: Union[Unset, bool] = UNSET
    blocked_tags: Union[Unset, List[str]] = UNSET
    is_tag_blocking_mode_inclusive: Union[Unset, bool] = UNSET
    include_tags: Union[Unset, List[str]] = UNSET
    enable_user_preference_access: Union[Unset, bool] = UNSET
    access_schedules: Union[Unset, List["ConfigurationAccessSchedule"]] = UNSET
    block_unrated_items: Union[Unset, List[ConfigurationUnratedItem]] = UNSET
    enable_remote_control_of_other_users: Union[Unset, bool] = UNSET
    enable_shared_device_control: Union[Unset, bool] = UNSET
    enable_remote_access: Union[Unset, bool] = UNSET
    enable_live_tv_management: Union[Unset, bool] = UNSET
    enable_live_tv_access: Union[Unset, bool] = UNSET
    enable_media_playback: Union[Unset, bool] = UNSET
    enable_audio_playback_transcoding: Union[Unset, bool] = UNSET
    enable_video_playback_transcoding: Union[Unset, bool] = UNSET
    enable_playback_remuxing: Union[Unset, bool] = UNSET
    enable_content_deletion: Union[Unset, bool] = UNSET
    restricted_features: Union[Unset, List[str]] = UNSET
    enable_content_deletion_from_folders: Union[Unset, List[str]] = UNSET
    enable_content_downloading: Union[Unset, bool] = UNSET
    enable_subtitle_downloading: Union[Unset, bool] = UNSET
    enable_subtitle_management: Union[Unset, bool] = UNSET
    enable_sync_transcoding: Union[Unset, bool] = UNSET
    enable_media_conversion: Union[Unset, bool] = UNSET
    enabled_channels: Union[Unset, List[str]] = UNSET
    enable_all_channels: Union[Unset, bool] = UNSET
    enabled_folders: Union[Unset, List[str]] = UNSET
    enable_all_folders: Union[Unset, bool] = UNSET
    invalid_login_attempt_count: Union[Unset, int] = UNSET
    enable_public_sharing: Union[Unset, bool] = UNSET
    blocked_media_folders: Union[Unset, List[str]] = UNSET
    remote_client_bitrate_limit: Union[Unset, int] = UNSET
    authentication_provider_id: Union[Unset, str] = UNSET
    excluded_sub_folders: Union[Unset, List[str]] = UNSET
    simultaneous_stream_limit: Union[Unset, int] = UNSET
    enabled_devices: Union[Unset, List[str]] = UNSET
    enable_all_devices: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_administrator = self.is_administrator
        is_hidden = self.is_hidden
        is_hidden_remotely = self.is_hidden_remotely
        is_hidden_from_unused_devices = self.is_hidden_from_unused_devices
        is_disabled = self.is_disabled
        max_parental_rating = self.max_parental_rating
        allow_tag_or_rating = self.allow_tag_or_rating
        blocked_tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.blocked_tags, Unset):
            blocked_tags = self.blocked_tags

        is_tag_blocking_mode_inclusive = self.is_tag_blocking_mode_inclusive
        include_tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.include_tags, Unset):
            include_tags = self.include_tags

        enable_user_preference_access = self.enable_user_preference_access
        access_schedules: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.access_schedules, Unset):
            access_schedules = []
            for access_schedules_item_data in self.access_schedules:
                access_schedules_item = access_schedules_item_data.to_dict()

                access_schedules.append(access_schedules_item)

        block_unrated_items: Union[Unset, List[str]] = UNSET
        if not isinstance(self.block_unrated_items, Unset):
            block_unrated_items = []
            for block_unrated_items_item_data in self.block_unrated_items:
                block_unrated_items_item = block_unrated_items_item_data.value

                block_unrated_items.append(block_unrated_items_item)

        enable_remote_control_of_other_users = self.enable_remote_control_of_other_users
        enable_shared_device_control = self.enable_shared_device_control
        enable_remote_access = self.enable_remote_access
        enable_live_tv_management = self.enable_live_tv_management
        enable_live_tv_access = self.enable_live_tv_access
        enable_media_playback = self.enable_media_playback
        enable_audio_playback_transcoding = self.enable_audio_playback_transcoding
        enable_video_playback_transcoding = self.enable_video_playback_transcoding
        enable_playback_remuxing = self.enable_playback_remuxing
        enable_content_deletion = self.enable_content_deletion
        restricted_features: Union[Unset, List[str]] = UNSET
        if not isinstance(self.restricted_features, Unset):
            restricted_features = self.restricted_features

        enable_content_deletion_from_folders: Union[Unset, List[str]] = UNSET
        if not isinstance(self.enable_content_deletion_from_folders, Unset):
            enable_content_deletion_from_folders = self.enable_content_deletion_from_folders

        enable_content_downloading = self.enable_content_downloading
        enable_subtitle_downloading = self.enable_subtitle_downloading
        enable_subtitle_management = self.enable_subtitle_management
        enable_sync_transcoding = self.enable_sync_transcoding
        enable_media_conversion = self.enable_media_conversion
        enabled_channels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.enabled_channels, Unset):
            enabled_channels = self.enabled_channels

        enable_all_channels = self.enable_all_channels
        enabled_folders: Union[Unset, List[str]] = UNSET
        if not isinstance(self.enabled_folders, Unset):
            enabled_folders = self.enabled_folders

        enable_all_folders = self.enable_all_folders
        invalid_login_attempt_count = self.invalid_login_attempt_count
        enable_public_sharing = self.enable_public_sharing
        blocked_media_folders: Union[Unset, List[str]] = UNSET
        if not isinstance(self.blocked_media_folders, Unset):
            blocked_media_folders = self.blocked_media_folders

        remote_client_bitrate_limit = self.remote_client_bitrate_limit
        authentication_provider_id = self.authentication_provider_id
        excluded_sub_folders: Union[Unset, List[str]] = UNSET
        if not isinstance(self.excluded_sub_folders, Unset):
            excluded_sub_folders = self.excluded_sub_folders

        simultaneous_stream_limit = self.simultaneous_stream_limit
        enabled_devices: Union[Unset, List[str]] = UNSET
        if not isinstance(self.enabled_devices, Unset):
            enabled_devices = self.enabled_devices

        enable_all_devices = self.enable_all_devices

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_administrator is not UNSET:
            field_dict["IsAdministrator"] = is_administrator
        if is_hidden is not UNSET:
            field_dict["IsHidden"] = is_hidden
        if is_hidden_remotely is not UNSET:
            field_dict["IsHiddenRemotely"] = is_hidden_remotely
        if is_hidden_from_unused_devices is not UNSET:
            field_dict["IsHiddenFromUnusedDevices"] = is_hidden_from_unused_devices
        if is_disabled is not UNSET:
            field_dict["IsDisabled"] = is_disabled
        if max_parental_rating is not UNSET:
            field_dict["MaxParentalRating"] = max_parental_rating
        if allow_tag_or_rating is not UNSET:
            field_dict["AllowTagOrRating"] = allow_tag_or_rating
        if blocked_tags is not UNSET:
            field_dict["BlockedTags"] = blocked_tags
        if is_tag_blocking_mode_inclusive is not UNSET:
            field_dict["IsTagBlockingModeInclusive"] = is_tag_blocking_mode_inclusive
        if include_tags is not UNSET:
            field_dict["IncludeTags"] = include_tags
        if enable_user_preference_access is not UNSET:
            field_dict["EnableUserPreferenceAccess"] = enable_user_preference_access
        if access_schedules is not UNSET:
            field_dict["AccessSchedules"] = access_schedules
        if block_unrated_items is not UNSET:
            field_dict["BlockUnratedItems"] = block_unrated_items
        if enable_remote_control_of_other_users is not UNSET:
            field_dict["EnableRemoteControlOfOtherUsers"] = enable_remote_control_of_other_users
        if enable_shared_device_control is not UNSET:
            field_dict["EnableSharedDeviceControl"] = enable_shared_device_control
        if enable_remote_access is not UNSET:
            field_dict["EnableRemoteAccess"] = enable_remote_access
        if enable_live_tv_management is not UNSET:
            field_dict["EnableLiveTvManagement"] = enable_live_tv_management
        if enable_live_tv_access is not UNSET:
            field_dict["EnableLiveTvAccess"] = enable_live_tv_access
        if enable_media_playback is not UNSET:
            field_dict["EnableMediaPlayback"] = enable_media_playback
        if enable_audio_playback_transcoding is not UNSET:
            field_dict["EnableAudioPlaybackTranscoding"] = enable_audio_playback_transcoding
        if enable_video_playback_transcoding is not UNSET:
            field_dict["EnableVideoPlaybackTranscoding"] = enable_video_playback_transcoding
        if enable_playback_remuxing is not UNSET:
            field_dict["EnablePlaybackRemuxing"] = enable_playback_remuxing
        if enable_content_deletion is not UNSET:
            field_dict["EnableContentDeletion"] = enable_content_deletion
        if restricted_features is not UNSET:
            field_dict["RestrictedFeatures"] = restricted_features
        if enable_content_deletion_from_folders is not UNSET:
            field_dict["EnableContentDeletionFromFolders"] = enable_content_deletion_from_folders
        if enable_content_downloading is not UNSET:
            field_dict["EnableContentDownloading"] = enable_content_downloading
        if enable_subtitle_downloading is not UNSET:
            field_dict["EnableSubtitleDownloading"] = enable_subtitle_downloading
        if enable_subtitle_management is not UNSET:
            field_dict["EnableSubtitleManagement"] = enable_subtitle_management
        if enable_sync_transcoding is not UNSET:
            field_dict["EnableSyncTranscoding"] = enable_sync_transcoding
        if enable_media_conversion is not UNSET:
            field_dict["EnableMediaConversion"] = enable_media_conversion
        if enabled_channels is not UNSET:
            field_dict["EnabledChannels"] = enabled_channels
        if enable_all_channels is not UNSET:
            field_dict["EnableAllChannels"] = enable_all_channels
        if enabled_folders is not UNSET:
            field_dict["EnabledFolders"] = enabled_folders
        if enable_all_folders is not UNSET:
            field_dict["EnableAllFolders"] = enable_all_folders
        if invalid_login_attempt_count is not UNSET:
            field_dict["InvalidLoginAttemptCount"] = invalid_login_attempt_count
        if enable_public_sharing is not UNSET:
            field_dict["EnablePublicSharing"] = enable_public_sharing
        if blocked_media_folders is not UNSET:
            field_dict["BlockedMediaFolders"] = blocked_media_folders
        if remote_client_bitrate_limit is not UNSET:
            field_dict["RemoteClientBitrateLimit"] = remote_client_bitrate_limit
        if authentication_provider_id is not UNSET:
            field_dict["AuthenticationProviderId"] = authentication_provider_id
        if excluded_sub_folders is not UNSET:
            field_dict["ExcludedSubFolders"] = excluded_sub_folders
        if simultaneous_stream_limit is not UNSET:
            field_dict["SimultaneousStreamLimit"] = simultaneous_stream_limit
        if enabled_devices is not UNSET:
            field_dict["EnabledDevices"] = enabled_devices
        if enable_all_devices is not UNSET:
            field_dict["EnableAllDevices"] = enable_all_devices

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.configuration_access_schedule import ConfigurationAccessSchedule

        d = src_dict.copy()
        is_administrator = d.pop("IsAdministrator", UNSET)

        is_hidden = d.pop("IsHidden", UNSET)

        is_hidden_remotely = d.pop("IsHiddenRemotely", UNSET)

        is_hidden_from_unused_devices = d.pop("IsHiddenFromUnusedDevices", UNSET)

        is_disabled = d.pop("IsDisabled", UNSET)

        max_parental_rating = d.pop("MaxParentalRating", UNSET)

        allow_tag_or_rating = d.pop("AllowTagOrRating", UNSET)

        blocked_tags = cast(List[str], d.pop("BlockedTags", UNSET))

        is_tag_blocking_mode_inclusive = d.pop("IsTagBlockingModeInclusive", UNSET)

        include_tags = cast(List[str], d.pop("IncludeTags", UNSET))

        enable_user_preference_access = d.pop("EnableUserPreferenceAccess", UNSET)

        access_schedules = []
        _access_schedules = d.pop("AccessSchedules", UNSET)
        for access_schedules_item_data in _access_schedules or []:
            access_schedules_item = ConfigurationAccessSchedule.from_dict(access_schedules_item_data)

            access_schedules.append(access_schedules_item)

        block_unrated_items = []
        _block_unrated_items = d.pop("BlockUnratedItems", UNSET)
        for block_unrated_items_item_data in _block_unrated_items or []:
            block_unrated_items_item = ConfigurationUnratedItem(block_unrated_items_item_data)

            block_unrated_items.append(block_unrated_items_item)

        enable_remote_control_of_other_users = d.pop("EnableRemoteControlOfOtherUsers", UNSET)

        enable_shared_device_control = d.pop("EnableSharedDeviceControl", UNSET)

        enable_remote_access = d.pop("EnableRemoteAccess", UNSET)

        enable_live_tv_management = d.pop("EnableLiveTvManagement", UNSET)

        enable_live_tv_access = d.pop("EnableLiveTvAccess", UNSET)

        enable_media_playback = d.pop("EnableMediaPlayback", UNSET)

        enable_audio_playback_transcoding = d.pop("EnableAudioPlaybackTranscoding", UNSET)

        enable_video_playback_transcoding = d.pop("EnableVideoPlaybackTranscoding", UNSET)

        enable_playback_remuxing = d.pop("EnablePlaybackRemuxing", UNSET)

        enable_content_deletion = d.pop("EnableContentDeletion", UNSET)

        restricted_features = cast(List[str], d.pop("RestrictedFeatures", UNSET))

        enable_content_deletion_from_folders = cast(List[str], d.pop("EnableContentDeletionFromFolders", UNSET))

        enable_content_downloading = d.pop("EnableContentDownloading", UNSET)

        enable_subtitle_downloading = d.pop("EnableSubtitleDownloading", UNSET)

        enable_subtitle_management = d.pop("EnableSubtitleManagement", UNSET)

        enable_sync_transcoding = d.pop("EnableSyncTranscoding", UNSET)

        enable_media_conversion = d.pop("EnableMediaConversion", UNSET)

        enabled_channels = cast(List[str], d.pop("EnabledChannels", UNSET))

        enable_all_channels = d.pop("EnableAllChannels", UNSET)

        enabled_folders = cast(List[str], d.pop("EnabledFolders", UNSET))

        enable_all_folders = d.pop("EnableAllFolders", UNSET)

        invalid_login_attempt_count = d.pop("InvalidLoginAttemptCount", UNSET)

        enable_public_sharing = d.pop("EnablePublicSharing", UNSET)

        blocked_media_folders = cast(List[str], d.pop("BlockedMediaFolders", UNSET))

        remote_client_bitrate_limit = d.pop("RemoteClientBitrateLimit", UNSET)

        authentication_provider_id = d.pop("AuthenticationProviderId", UNSET)

        excluded_sub_folders = cast(List[str], d.pop("ExcludedSubFolders", UNSET))

        simultaneous_stream_limit = d.pop("SimultaneousStreamLimit", UNSET)

        enabled_devices = cast(List[str], d.pop("EnabledDevices", UNSET))

        enable_all_devices = d.pop("EnableAllDevices", UNSET)

        users_user_policy = cls(
            is_administrator=is_administrator,
            is_hidden=is_hidden,
            is_hidden_remotely=is_hidden_remotely,
            is_hidden_from_unused_devices=is_hidden_from_unused_devices,
            is_disabled=is_disabled,
            max_parental_rating=max_parental_rating,
            allow_tag_or_rating=allow_tag_or_rating,
            blocked_tags=blocked_tags,
            is_tag_blocking_mode_inclusive=is_tag_blocking_mode_inclusive,
            include_tags=include_tags,
            enable_user_preference_access=enable_user_preference_access,
            access_schedules=access_schedules,
            block_unrated_items=block_unrated_items,
            enable_remote_control_of_other_users=enable_remote_control_of_other_users,
            enable_shared_device_control=enable_shared_device_control,
            enable_remote_access=enable_remote_access,
            enable_live_tv_management=enable_live_tv_management,
            enable_live_tv_access=enable_live_tv_access,
            enable_media_playback=enable_media_playback,
            enable_audio_playback_transcoding=enable_audio_playback_transcoding,
            enable_video_playback_transcoding=enable_video_playback_transcoding,
            enable_playback_remuxing=enable_playback_remuxing,
            enable_content_deletion=enable_content_deletion,
            restricted_features=restricted_features,
            enable_content_deletion_from_folders=enable_content_deletion_from_folders,
            enable_content_downloading=enable_content_downloading,
            enable_subtitle_downloading=enable_subtitle_downloading,
            enable_subtitle_management=enable_subtitle_management,
            enable_sync_transcoding=enable_sync_transcoding,
            enable_media_conversion=enable_media_conversion,
            enabled_channels=enabled_channels,
            enable_all_channels=enable_all_channels,
            enabled_folders=enabled_folders,
            enable_all_folders=enable_all_folders,
            invalid_login_attempt_count=invalid_login_attempt_count,
            enable_public_sharing=enable_public_sharing,
            blocked_media_folders=blocked_media_folders,
            remote_client_bitrate_limit=remote_client_bitrate_limit,
            authentication_provider_id=authentication_provider_id,
            excluded_sub_folders=excluded_sub_folders,
            simultaneous_stream_limit=simultaneous_stream_limit,
            enabled_devices=enabled_devices,
            enable_all_devices=enable_all_devices,
        )

        users_user_policy.additional_properties = d
        return users_user_policy

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
