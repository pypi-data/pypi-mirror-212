""" Contains all the data models used in inputs/outputs """

from .activity_log_entry import ActivityLogEntry
from .all_theme_media_result import AllThemeMediaResult
from .api_base_items_request import ApiBaseItemsRequest
from .attributes_simple_condition import AttributesSimpleCondition
from .attributes_value_condition import AttributesValueCondition
from .authenticate_user import AuthenticateUser
from .authenticate_user_by_name import AuthenticateUserByName
from .authentication_authentication_result import AuthenticationAuthenticationResult
from .base_item_dto import BaseItemDto
from .base_item_dto_image_tags import BaseItemDtoImageTags
from .base_item_person import BaseItemPerson
from .branding_branding_options import BrandingBrandingOptions
from .chapter_info import ChapterInfo
from .client_capabilities import ClientCapabilities
from .collections_collection_creation_result import CollectionsCollectionCreationResult
from .common_plugins_i_plugin import CommonPluginsIPlugin
from .configuration_access_schedule import ConfigurationAccessSchedule
from .configuration_codec_configuration import ConfigurationCodecConfiguration
from .configuration_dynamic_day_of_week import ConfigurationDynamicDayOfWeek
from .configuration_image_option import ConfigurationImageOption
from .configuration_image_saving_convention import ConfigurationImageSavingConvention
from .configuration_library_options import ConfigurationLibraryOptions
from .configuration_media_path_info import ConfigurationMediaPathInfo
from .configuration_metadata_features import ConfigurationMetadataFeatures
from .configuration_path_substitution import ConfigurationPathSubstitution
from .configuration_segment_skip_mode import ConfigurationSegmentSkipMode
from .configuration_server_configuration import ConfigurationServerConfiguration
from .configuration_subtitle_playback_mode import ConfigurationSubtitlePlaybackMode
from .configuration_type_options import ConfigurationTypeOptions
from .configuration_unrated_item import ConfigurationUnratedItem
from .configuration_user_configuration import ConfigurationUserConfiguration
from .connect_connect_authentication_exchange_result import ConnectConnectAuthenticationExchangeResult
from .connect_user_link_result import ConnectUserLinkResult
from .connect_user_link_type import ConnectUserLinkType
from .create_user_by_name import CreateUserByName
from .day_of_week import DayOfWeek
from .default_directory_browser_info import DefaultDirectoryBrowserInfo
from .devices_content_upload_history import DevicesContentUploadHistory
from .devices_device_info import DevicesDeviceInfo
from .devices_device_options import DevicesDeviceOptions
from .devices_local_file_info import DevicesLocalFileInfo
from .display_preferences import DisplayPreferences
from .display_preferences_custom_prefs import DisplayPreferencesCustomPrefs
from .dlna_codec_profile import DlnaCodecProfile
from .dlna_codec_type import DlnaCodecType
from .dlna_container_profile import DlnaContainerProfile
from .dlna_device_profile import DlnaDeviceProfile
from .dlna_direct_play_profile import DlnaDirectPlayProfile
from .dlna_dlna_profile_type import DlnaDlnaProfileType
from .dlna_encoding_context import DlnaEncodingContext
from .dlna_playback_error_code import DlnaPlaybackErrorCode
from .dlna_profile_condition import DlnaProfileCondition
from .dlna_profile_condition_type import DlnaProfileConditionType
from .dlna_profile_condition_value import DlnaProfileConditionValue
from .dlna_response_profile import DlnaResponseProfile
from .dlna_subtitle_delivery_method import DlnaSubtitleDeliveryMethod
from .dlna_subtitle_profile import DlnaSubtitleProfile
from .dlna_transcode_seek_info import DlnaTranscodeSeekInfo
from .dlna_transcoding_profile import DlnaTranscodingProfile
from .drawing_image_orientation import DrawingImageOrientation
from .emby_dlna_profiles_device_identification import EmbyDlnaProfilesDeviceIdentification
from .emby_dlna_profiles_device_profile_type import EmbyDlnaProfilesDeviceProfileType
from .emby_dlna_profiles_dlna_profile import EmbyDlnaProfilesDlnaProfile
from .emby_dlna_profiles_header_match_type import EmbyDlnaProfilesHeaderMatchType
from .emby_dlna_profiles_http_header_info import EmbyDlnaProfilesHttpHeaderInfo
from .emby_dlna_profiles_protocol_info_detection import EmbyDlnaProfilesProtocolInfoDetection
from .emby_features_feature_info import EmbyFeaturesFeatureInfo
from .emby_features_feature_type import EmbyFeaturesFeatureType
from .emby_live_tv_channel_management_info import EmbyLiveTVChannelManagementInfo
from .emby_media_model_enums_codec_directions import EmbyMediaModelEnumsCodecDirections
from .emby_media_model_enums_codec_kinds import EmbyMediaModelEnumsCodecKinds
from .emby_media_model_enums_color_formats import EmbyMediaModelEnumsColorFormats
from .emby_media_model_enums_secondary_frameworks import EmbyMediaModelEnumsSecondaryFrameworks
from .emby_media_model_enums_video_media_types import EmbyMediaModelEnumsVideoMediaTypes
from .emby_media_model_types_bit_rate import EmbyMediaModelTypesBitRate
from .emby_media_model_types_level_information import EmbyMediaModelTypesLevelInformation
from .emby_media_model_types_profile_information import EmbyMediaModelTypesProfileInformation
from .emby_media_model_types_profile_level_information import EmbyMediaModelTypesProfileLevelInformation
from .emby_media_model_types_resolution import EmbyMediaModelTypesResolution
from .emby_media_model_types_resolution_with_rate import EmbyMediaModelTypesResolutionWithRate
from .emby_notifications_notification_category_info import EmbyNotificationsNotificationCategoryInfo
from .emby_notifications_notification_type_info import EmbyNotificationsNotificationTypeInfo
from .emby_notifications_user_notification_info import EmbyNotificationsUserNotificationInfo
from .emby_notifications_user_notification_info_options import EmbyNotificationsUserNotificationInfoOptions
from .emby_web_api_configuration_page_info import EmbyWebApiConfigurationPageInfo
from .emby_web_generic_edit_actions_postback_action import EmbyWebGenericEditActionsPostbackAction
from .emby_web_generic_edit_common_editor_types import EmbyWebGenericEditCommonEditorTypes
from .emby_web_generic_edit_conditions_property_condition import EmbyWebGenericEditConditionsPropertyCondition
from .emby_web_generic_edit_conditions_property_condition_type import EmbyWebGenericEditConditionsPropertyConditionType
from .emby_web_generic_edit_conditions_property_condition_value import (
    EmbyWebGenericEditConditionsPropertyConditionValue,
)
from .emby_web_generic_edit_edit_object_container import EmbyWebGenericEditEditObjectContainer
from .emby_web_generic_edit_edit_object_container_default_object import (
    EmbyWebGenericEditEditObjectContainerDefaultObject,
)
from .emby_web_generic_edit_edit_object_container_object import EmbyWebGenericEditEditObjectContainerObject
from .emby_web_generic_edit_editors_editor_base import EmbyWebGenericEditEditorsEditorBase
from .emby_web_generic_edit_editors_editor_button_item import EmbyWebGenericEditEditorsEditorButtonItem
from .emby_web_generic_edit_editors_editor_root import EmbyWebGenericEditEditorsEditorRoot
from .emby_web_generic_ui_api_endpoints_run_ui_command import EmbyWebGenericUIApiEndpointsRunUICommand
from .emby_web_generic_ui_model_enums_ui_command_type import EmbyWebGenericUIModelEnumsUICommandType
from .emby_web_generic_ui_model_enums_ui_view_type import EmbyWebGenericUIModelEnumsUIViewType
from .emby_web_generic_ui_model_ui_command import EmbyWebGenericUIModelUICommand
from .emby_web_generic_ui_model_ui_tab_page_info import EmbyWebGenericUIModelUITabPageInfo
from .emby_web_generic_ui_model_ui_view_info import EmbyWebGenericUIModelUIViewInfo
from .extended_video_sub_types import ExtendedVideoSubTypes
from .extended_video_types import ExtendedVideoTypes
from .external_id_info import ExternalIdInfo
from .external_url import ExternalUrl
from .forgot_password import ForgotPassword
from .forgot_password_pin import ForgotPasswordPin
from .general_command import GeneralCommand
from .general_command_arguments import GeneralCommandArguments
from .generic_edit_i_edit_object_container import GenericEditIEditObjectContainer
from .generic_edit_i_edit_object_container_default_object import GenericEditIEditObjectContainerDefaultObject
from .generic_edit_i_edit_object_container_object import GenericEditIEditObjectContainerObject
from .globalization_country_info import GlobalizationCountryInfo
from .globalization_culture_dto import GlobalizationCultureDto
from .globalization_localizaton_option import GlobalizationLocalizatonOption
from .image_info import ImageInfo
from .image_provider_info import ImageProviderInfo
from .image_type import ImageType
from .io_file_system_entry_info import IOFileSystemEntryInfo
from .io_file_system_entry_type import IOFileSystemEntryType
from .item_counts import ItemCounts
from .library_add_media_path import LibraryAddMediaPath
from .library_add_virtual_folder import LibraryAddVirtualFolder
from .library_delete_info import LibraryDeleteInfo
from .library_item_link_type import LibraryItemLinkType
from .library_library_option_info import LibraryLibraryOptionInfo
from .library_library_options_result import LibraryLibraryOptionsResult
from .library_library_type_options import LibraryLibraryTypeOptions
from .library_media_folder import LibraryMediaFolder
from .library_media_update_info import LibraryMediaUpdateInfo
from .library_post_updated_media import LibraryPostUpdatedMedia
from .library_remove_media_path import LibraryRemoveMediaPath
from .library_remove_virtual_folder import LibraryRemoveVirtualFolder
from .library_rename_virtual_folder import LibraryRenameVirtualFolder
from .library_sub_folder import LibrarySubFolder
from .library_update_library_options import LibraryUpdateLibraryOptions
from .library_update_media_path import LibraryUpdateMediaPath
from .library_user_copy_options import LibraryUserCopyOptions
from .live_tv_api_epg_row import LiveTVApiEpgRow
from .live_tv_api_listing_provider_type_info import LiveTVApiListingProviderTypeInfo
from .live_tv_api_set_channel_disabled import LiveTVApiSetChannelDisabled
from .live_tv_api_set_channel_mapping import LiveTVApiSetChannelMapping
from .live_tv_api_set_channel_sort_index import LiveTVApiSetChannelSortIndex
from .live_tv_api_tag_item import LiveTVApiTagItem
from .live_tv_channel_type import LiveTvChannelType
from .live_tv_guide_info import LiveTvGuideInfo
from .live_tv_keep_until import LiveTvKeepUntil
from .live_tv_keyword_info import LiveTvKeywordInfo
from .live_tv_keyword_type import LiveTvKeywordType
from .live_tv_listings_provider_info import LiveTvListingsProviderInfo
from .live_tv_live_tv_info import LiveTvLiveTvInfo
from .live_tv_recording_status import LiveTvRecordingStatus
from .live_tv_series_timer_info import LiveTvSeriesTimerInfo
from .live_tv_series_timer_info_dto import LiveTvSeriesTimerInfoDto
from .live_tv_series_timer_info_dto_image_tags import LiveTvSeriesTimerInfoDtoImageTags
from .live_tv_timer_info_dto import LiveTvTimerInfoDto
from .live_tv_timer_type import LiveTvTimerType
from .live_tv_tuner_host_info import LiveTvTunerHostInfo
from .location_type import LocationType
from .log_file import LogFile
from .logging_log_severity import LoggingLogSeverity
from .marker_type import MarkerType
from .media_encoding_api_on_playback_progress import MediaEncodingApiOnPlaybackProgress
from .media_encoding_codec_parameter_context import MediaEncodingCodecParameterContext
from .media_encoding_codecs_common_interfaces_i_codec_device_capabilities import (
    MediaEncodingCodecsCommonInterfacesICodecDeviceCapabilities,
)
from .media_encoding_codecs_common_interfaces_i_codec_device_info import (
    MediaEncodingCodecsCommonInterfacesICodecDeviceInfo,
)
from .media_encoding_codecs_video_codecs_video_codec_base import MediaEncodingCodecsVideoCodecsVideoCodecBase
from .media_encoding_configuration_tone_mapping_tone_map_options_visibility import (
    MediaEncodingConfigurationToneMappingToneMapOptionsVisibility,
)
from .media_info_live_stream_request import MediaInfoLiveStreamRequest
from .media_info_live_stream_response import MediaInfoLiveStreamResponse
from .media_info_media_protocol import MediaInfoMediaProtocol
from .media_info_playback_info_request import MediaInfoPlaybackInfoRequest
from .media_info_playback_info_response import MediaInfoPlaybackInfoResponse
from .media_info_transport_stream_timestamp import MediaInfoTransportStreamTimestamp
from .media_source_info import MediaSourceInfo
from .media_source_info_required_http_headers import MediaSourceInfoRequiredHttpHeaders
from .media_source_type import MediaSourceType
from .media_stream import MediaStream
from .media_stream_type import MediaStreamType
from .media_url import MediaUrl
from .metadata_editor_info import MetadataEditorInfo
from .metadata_fields import MetadataFields
from .name_id_pair import NameIdPair
from .name_long_id_pair import NameLongIdPair
from .name_value_pair import NameValuePair
from .net_end_point_info import NetEndPointInfo
from .operating_system import OperatingSystem
from .parental_rating import ParentalRating
from .persistence_intro_debug_info import PersistenceIntroDebugInfo
from .person_type import PersonType
from .play_command import PlayCommand
from .play_method import PlayMethod
from .play_request import PlayRequest
from .playback_progress_info import PlaybackProgressInfo
from .playback_start_info import PlaybackStartInfo
from .playback_stop_info import PlaybackStopInfo
from .player_state_info import PlayerStateInfo
from .playlists_add_to_playlist_result import PlaylistsAddToPlaylistResult
from .playlists_playlist_creation_result import PlaylistsPlaylistCreationResult
from .playstate_command import PlaystateCommand
from .playstate_request import PlaystateRequest
from .plugins_configuration_page_type import PluginsConfigurationPageType
from .plugins_plugin_info import PluginsPluginInfo
from .process_run_metrics_process_metric_point import ProcessRunMetricsProcessMetricPoint
from .process_run_metrics_process_statistics import ProcessRunMetricsProcessStatistics
from .progress_event import ProgressEvent
from .provider_id_dictionary import ProviderIdDictionary
from .providers_album_info import ProvidersAlbumInfo
from .providers_artist_info import ProvidersArtistInfo
from .providers_book_info import ProvidersBookInfo
from .providers_game_info import ProvidersGameInfo
from .providers_item_lookup_info import ProvidersItemLookupInfo
from .providers_metadata_refresh_mode import ProvidersMetadataRefreshMode
from .providers_movie_info import ProvidersMovieInfo
from .providers_music_video_info import ProvidersMusicVideoInfo
from .providers_person_lookup_info import ProvidersPersonLookupInfo
from .providers_remote_search_query_providers_album_info import ProvidersRemoteSearchQueryProvidersAlbumInfo
from .providers_remote_search_query_providers_artist_info import ProvidersRemoteSearchQueryProvidersArtistInfo
from .providers_remote_search_query_providers_book_info import ProvidersRemoteSearchQueryProvidersBookInfo
from .providers_remote_search_query_providers_game_info import ProvidersRemoteSearchQueryProvidersGameInfo
from .providers_remote_search_query_providers_item_lookup_info import ProvidersRemoteSearchQueryProvidersItemLookupInfo
from .providers_remote_search_query_providers_movie_info import ProvidersRemoteSearchQueryProvidersMovieInfo
from .providers_remote_search_query_providers_music_video_info import ProvidersRemoteSearchQueryProvidersMusicVideoInfo
from .providers_remote_search_query_providers_person_lookup_info import (
    ProvidersRemoteSearchQueryProvidersPersonLookupInfo,
)
from .providers_remote_search_query_providers_series_info import ProvidersRemoteSearchQueryProvidersSeriesInfo
from .providers_remote_search_query_providers_trailer_info import ProvidersRemoteSearchQueryProvidersTrailerInfo
from .providers_series_info import ProvidersSeriesInfo
from .providers_song_info import ProvidersSongInfo
from .providers_trailer_info import ProvidersTrailerInfo
from .public_system_info import PublicSystemInfo
from .query_result_activity_log_entry import QueryResultActivityLogEntry
from .query_result_base_item_dto import QueryResultBaseItemDto
from .query_result_devices_device_info import QueryResultDevicesDeviceInfo
from .query_result_emby_live_tv_channel_management_info import QueryResultEmbyLiveTVChannelManagementInfo
from .query_result_live_tv_api_epg_row import QueryResultLiveTVApiEpgRow
from .query_result_live_tv_series_timer_info_dto import QueryResultLiveTvSeriesTimerInfoDto
from .query_result_live_tv_timer_info_dto import QueryResultLiveTvTimerInfoDto
from .query_result_log_file import QueryResultLogFile
from .query_result_string import QueryResultString
from .query_result_sync_model_sync_job_item import QueryResultSyncModelSyncJobItem
from .query_result_sync_sync_job import QueryResultSyncSyncJob
from .query_result_user_dto import QueryResultUserDto
from .query_result_user_library_official_rating_item import QueryResultUserLibraryOfficialRatingItem
from .query_result_user_library_tag_item import QueryResultUserLibraryTagItem
from .query_result_virtual_folder_info import QueryResultVirtualFolderInfo
from .queue_item import QueueItem
from .rating_type import RatingType
from .recommendation_dto import RecommendationDto
from .recommendation_type import RecommendationType
from .remote_image_info import RemoteImageInfo
from .remote_image_result import RemoteImageResult
from .remote_search_result import RemoteSearchResult
from .remote_subtitle_info import RemoteSubtitleInfo
from .repeat_mode import RepeatMode
from .roku_metadata_api_thumbnail_info import RokuMetadataApiThumbnailInfo
from .roku_metadata_api_thumbnail_set_info import RokuMetadataApiThumbnailSetInfo
from .series_display_order import SeriesDisplayOrder
from .session_session_info import SessionSessionInfo
from .session_user_info import SessionUserInfo
from .sort_order import SortOrder
from .subtitle_location_type import SubtitleLocationType
from .subtitles_subtitle_download_result import SubtitlesSubtitleDownloadResult
from .sync_model_item_file_info import SyncModelItemFileInfo
from .sync_model_item_file_type import SyncModelItemFileType
from .sync_model_sync_data_request import SyncModelSyncDataRequest
from .sync_model_sync_data_response import SyncModelSyncDataResponse
from .sync_model_sync_dialog_options import SyncModelSyncDialogOptions
from .sync_model_sync_job_creation_result import SyncModelSyncJobCreationResult
from .sync_model_sync_job_item import SyncModelSyncJobItem
from .sync_model_sync_job_item_status import SyncModelSyncJobItemStatus
from .sync_model_sync_job_option import SyncModelSyncJobOption
from .sync_model_sync_job_request import SyncModelSyncJobRequest
from .sync_model_sync_profile_option import SyncModelSyncProfileOption
from .sync_model_sync_quality_option import SyncModelSyncQualityOption
from .sync_model_synced_item import SyncModelSyncedItem
from .sync_model_synced_item_progress import SyncModelSyncedItemProgress
from .sync_sync_category import SyncSyncCategory
from .sync_sync_job import SyncSyncJob
from .sync_sync_job_status import SyncSyncJobStatus
from .sync_sync_target import SyncSyncTarget
from .system_info import SystemInfo
from .tasks_system_event import TasksSystemEvent
from .tasks_task_completion_status import TasksTaskCompletionStatus
from .tasks_task_info import TasksTaskInfo
from .tasks_task_result import TasksTaskResult
from .tasks_task_state import TasksTaskState
from .tasks_task_trigger_info import TasksTaskTriggerInfo
from .theme_media_result import ThemeMediaResult
from .time_span import TimeSpan
from .transcode_reason import TranscodeReason
from .transcoding_info import TranscodingInfo
from .transcoding_vp_step_info import TranscodingVpStepInfo
from .transcoding_vp_step_types import TranscodingVpStepTypes
from .tuple_double_double import TupleDoubleDouble
from .update_user_easy_password import UpdateUserEasyPassword
from .update_user_password import UpdateUserPassword
from .updates_installation_info import UpdatesInstallationInfo
from .updates_package_info import UpdatesPackageInfo
from .updates_package_target_system import UpdatesPackageTargetSystem
from .updates_package_version_class import UpdatesPackageVersionClass
from .updates_package_version_info import UpdatesPackageVersionInfo
from .user_dto import UserDto
from .user_item_data_dto import UserItemDataDto
from .user_library_add_tags import UserLibraryAddTags
from .user_library_official_rating_item import UserLibraryOfficialRatingItem
from .user_library_tag_item import UserLibraryTagItem
from .users_forgot_password_action import UsersForgotPasswordAction
from .users_forgot_password_result import UsersForgotPasswordResult
from .users_pin_redeem_result import UsersPinRedeemResult
from .users_user_action import UsersUserAction
from .users_user_action_type import UsersUserActionType
from .users_user_policy import UsersUserPolicy
from .validate_path import ValidatePath
from .version import Version
from .video_3d_format import Video3DFormat
from .virtual_folder_info import VirtualFolderInfo
from .wake_on_lan_info import WakeOnLanInfo

__all__ = (
    "ActivityLogEntry",
    "AllThemeMediaResult",
    "ApiBaseItemsRequest",
    "AttributesSimpleCondition",
    "AttributesValueCondition",
    "AuthenticateUser",
    "AuthenticateUserByName",
    "AuthenticationAuthenticationResult",
    "BaseItemDto",
    "BaseItemDtoImageTags",
    "BaseItemPerson",
    "BrandingBrandingOptions",
    "ChapterInfo",
    "ClientCapabilities",
    "CollectionsCollectionCreationResult",
    "CommonPluginsIPlugin",
    "ConfigurationAccessSchedule",
    "ConfigurationCodecConfiguration",
    "ConfigurationDynamicDayOfWeek",
    "ConfigurationImageOption",
    "ConfigurationImageSavingConvention",
    "ConfigurationLibraryOptions",
    "ConfigurationMediaPathInfo",
    "ConfigurationMetadataFeatures",
    "ConfigurationPathSubstitution",
    "ConfigurationSegmentSkipMode",
    "ConfigurationServerConfiguration",
    "ConfigurationSubtitlePlaybackMode",
    "ConfigurationTypeOptions",
    "ConfigurationUnratedItem",
    "ConfigurationUserConfiguration",
    "ConnectConnectAuthenticationExchangeResult",
    "ConnectUserLinkResult",
    "ConnectUserLinkType",
    "CreateUserByName",
    "DayOfWeek",
    "DefaultDirectoryBrowserInfo",
    "DevicesContentUploadHistory",
    "DevicesDeviceInfo",
    "DevicesDeviceOptions",
    "DevicesLocalFileInfo",
    "DisplayPreferences",
    "DisplayPreferencesCustomPrefs",
    "DlnaCodecProfile",
    "DlnaCodecType",
    "DlnaContainerProfile",
    "DlnaDeviceProfile",
    "DlnaDirectPlayProfile",
    "DlnaDlnaProfileType",
    "DlnaEncodingContext",
    "DlnaPlaybackErrorCode",
    "DlnaProfileCondition",
    "DlnaProfileConditionType",
    "DlnaProfileConditionValue",
    "DlnaResponseProfile",
    "DlnaSubtitleDeliveryMethod",
    "DlnaSubtitleProfile",
    "DlnaTranscodeSeekInfo",
    "DlnaTranscodingProfile",
    "DrawingImageOrientation",
    "EmbyDlnaProfilesDeviceIdentification",
    "EmbyDlnaProfilesDeviceProfileType",
    "EmbyDlnaProfilesDlnaProfile",
    "EmbyDlnaProfilesHeaderMatchType",
    "EmbyDlnaProfilesHttpHeaderInfo",
    "EmbyDlnaProfilesProtocolInfoDetection",
    "EmbyFeaturesFeatureInfo",
    "EmbyFeaturesFeatureType",
    "EmbyLiveTVChannelManagementInfo",
    "EmbyMediaModelEnumsCodecDirections",
    "EmbyMediaModelEnumsCodecKinds",
    "EmbyMediaModelEnumsColorFormats",
    "EmbyMediaModelEnumsSecondaryFrameworks",
    "EmbyMediaModelEnumsVideoMediaTypes",
    "EmbyMediaModelTypesBitRate",
    "EmbyMediaModelTypesLevelInformation",
    "EmbyMediaModelTypesProfileInformation",
    "EmbyMediaModelTypesProfileLevelInformation",
    "EmbyMediaModelTypesResolution",
    "EmbyMediaModelTypesResolutionWithRate",
    "EmbyNotificationsNotificationCategoryInfo",
    "EmbyNotificationsNotificationTypeInfo",
    "EmbyNotificationsUserNotificationInfo",
    "EmbyNotificationsUserNotificationInfoOptions",
    "EmbyWebApiConfigurationPageInfo",
    "EmbyWebGenericEditActionsPostbackAction",
    "EmbyWebGenericEditCommonEditorTypes",
    "EmbyWebGenericEditConditionsPropertyCondition",
    "EmbyWebGenericEditConditionsPropertyConditionType",
    "EmbyWebGenericEditConditionsPropertyConditionValue",
    "EmbyWebGenericEditEditObjectContainer",
    "EmbyWebGenericEditEditObjectContainerDefaultObject",
    "EmbyWebGenericEditEditObjectContainerObject",
    "EmbyWebGenericEditEditorsEditorBase",
    "EmbyWebGenericEditEditorsEditorButtonItem",
    "EmbyWebGenericEditEditorsEditorRoot",
    "EmbyWebGenericUIApiEndpointsRunUICommand",
    "EmbyWebGenericUIModelEnumsUICommandType",
    "EmbyWebGenericUIModelEnumsUIViewType",
    "EmbyWebGenericUIModelUICommand",
    "EmbyWebGenericUIModelUITabPageInfo",
    "EmbyWebGenericUIModelUIViewInfo",
    "ExtendedVideoSubTypes",
    "ExtendedVideoTypes",
    "ExternalIdInfo",
    "ExternalUrl",
    "ForgotPassword",
    "ForgotPasswordPin",
    "GeneralCommand",
    "GeneralCommandArguments",
    "GenericEditIEditObjectContainer",
    "GenericEditIEditObjectContainerDefaultObject",
    "GenericEditIEditObjectContainerObject",
    "GlobalizationCountryInfo",
    "GlobalizationCultureDto",
    "GlobalizationLocalizatonOption",
    "ImageInfo",
    "ImageProviderInfo",
    "ImageType",
    "IOFileSystemEntryInfo",
    "IOFileSystemEntryType",
    "ItemCounts",
    "LibraryAddMediaPath",
    "LibraryAddVirtualFolder",
    "LibraryDeleteInfo",
    "LibraryItemLinkType",
    "LibraryLibraryOptionInfo",
    "LibraryLibraryOptionsResult",
    "LibraryLibraryTypeOptions",
    "LibraryMediaFolder",
    "LibraryMediaUpdateInfo",
    "LibraryPostUpdatedMedia",
    "LibraryRemoveMediaPath",
    "LibraryRemoveVirtualFolder",
    "LibraryRenameVirtualFolder",
    "LibrarySubFolder",
    "LibraryUpdateLibraryOptions",
    "LibraryUpdateMediaPath",
    "LibraryUserCopyOptions",
    "LiveTVApiEpgRow",
    "LiveTVApiListingProviderTypeInfo",
    "LiveTVApiSetChannelDisabled",
    "LiveTVApiSetChannelMapping",
    "LiveTVApiSetChannelSortIndex",
    "LiveTVApiTagItem",
    "LiveTvChannelType",
    "LiveTvGuideInfo",
    "LiveTvKeepUntil",
    "LiveTvKeywordInfo",
    "LiveTvKeywordType",
    "LiveTvListingsProviderInfo",
    "LiveTvLiveTvInfo",
    "LiveTvRecordingStatus",
    "LiveTvSeriesTimerInfo",
    "LiveTvSeriesTimerInfoDto",
    "LiveTvSeriesTimerInfoDtoImageTags",
    "LiveTvTimerInfoDto",
    "LiveTvTimerType",
    "LiveTvTunerHostInfo",
    "LocationType",
    "LogFile",
    "LoggingLogSeverity",
    "MarkerType",
    "MediaEncodingApiOnPlaybackProgress",
    "MediaEncodingCodecParameterContext",
    "MediaEncodingCodecsCommonInterfacesICodecDeviceCapabilities",
    "MediaEncodingCodecsCommonInterfacesICodecDeviceInfo",
    "MediaEncodingCodecsVideoCodecsVideoCodecBase",
    "MediaEncodingConfigurationToneMappingToneMapOptionsVisibility",
    "MediaInfoLiveStreamRequest",
    "MediaInfoLiveStreamResponse",
    "MediaInfoMediaProtocol",
    "MediaInfoPlaybackInfoRequest",
    "MediaInfoPlaybackInfoResponse",
    "MediaInfoTransportStreamTimestamp",
    "MediaSourceInfo",
    "MediaSourceInfoRequiredHttpHeaders",
    "MediaSourceType",
    "MediaStream",
    "MediaStreamType",
    "MediaUrl",
    "MetadataEditorInfo",
    "MetadataFields",
    "NameIdPair",
    "NameLongIdPair",
    "NameValuePair",
    "NetEndPointInfo",
    "OperatingSystem",
    "ParentalRating",
    "PersistenceIntroDebugInfo",
    "PersonType",
    "PlaybackProgressInfo",
    "PlaybackStartInfo",
    "PlaybackStopInfo",
    "PlayCommand",
    "PlayerStateInfo",
    "PlaylistsAddToPlaylistResult",
    "PlaylistsPlaylistCreationResult",
    "PlayMethod",
    "PlayRequest",
    "PlaystateCommand",
    "PlaystateRequest",
    "PluginsConfigurationPageType",
    "PluginsPluginInfo",
    "ProcessRunMetricsProcessMetricPoint",
    "ProcessRunMetricsProcessStatistics",
    "ProgressEvent",
    "ProviderIdDictionary",
    "ProvidersAlbumInfo",
    "ProvidersArtistInfo",
    "ProvidersBookInfo",
    "ProvidersGameInfo",
    "ProvidersItemLookupInfo",
    "ProvidersMetadataRefreshMode",
    "ProvidersMovieInfo",
    "ProvidersMusicVideoInfo",
    "ProvidersPersonLookupInfo",
    "ProvidersRemoteSearchQueryProvidersAlbumInfo",
    "ProvidersRemoteSearchQueryProvidersArtistInfo",
    "ProvidersRemoteSearchQueryProvidersBookInfo",
    "ProvidersRemoteSearchQueryProvidersGameInfo",
    "ProvidersRemoteSearchQueryProvidersItemLookupInfo",
    "ProvidersRemoteSearchQueryProvidersMovieInfo",
    "ProvidersRemoteSearchQueryProvidersMusicVideoInfo",
    "ProvidersRemoteSearchQueryProvidersPersonLookupInfo",
    "ProvidersRemoteSearchQueryProvidersSeriesInfo",
    "ProvidersRemoteSearchQueryProvidersTrailerInfo",
    "ProvidersSeriesInfo",
    "ProvidersSongInfo",
    "ProvidersTrailerInfo",
    "PublicSystemInfo",
    "QueryResultActivityLogEntry",
    "QueryResultBaseItemDto",
    "QueryResultDevicesDeviceInfo",
    "QueryResultEmbyLiveTVChannelManagementInfo",
    "QueryResultLiveTVApiEpgRow",
    "QueryResultLiveTvSeriesTimerInfoDto",
    "QueryResultLiveTvTimerInfoDto",
    "QueryResultLogFile",
    "QueryResultString",
    "QueryResultSyncModelSyncJobItem",
    "QueryResultSyncSyncJob",
    "QueryResultUserDto",
    "QueryResultUserLibraryOfficialRatingItem",
    "QueryResultUserLibraryTagItem",
    "QueryResultVirtualFolderInfo",
    "QueueItem",
    "RatingType",
    "RecommendationDto",
    "RecommendationType",
    "RemoteImageInfo",
    "RemoteImageResult",
    "RemoteSearchResult",
    "RemoteSubtitleInfo",
    "RepeatMode",
    "RokuMetadataApiThumbnailInfo",
    "RokuMetadataApiThumbnailSetInfo",
    "SeriesDisplayOrder",
    "SessionSessionInfo",
    "SessionUserInfo",
    "SortOrder",
    "SubtitleLocationType",
    "SubtitlesSubtitleDownloadResult",
    "SyncModelItemFileInfo",
    "SyncModelItemFileType",
    "SyncModelSyncDataRequest",
    "SyncModelSyncDataResponse",
    "SyncModelSyncDialogOptions",
    "SyncModelSyncedItem",
    "SyncModelSyncedItemProgress",
    "SyncModelSyncJobCreationResult",
    "SyncModelSyncJobItem",
    "SyncModelSyncJobItemStatus",
    "SyncModelSyncJobOption",
    "SyncModelSyncJobRequest",
    "SyncModelSyncProfileOption",
    "SyncModelSyncQualityOption",
    "SyncSyncCategory",
    "SyncSyncJob",
    "SyncSyncJobStatus",
    "SyncSyncTarget",
    "SystemInfo",
    "TasksSystemEvent",
    "TasksTaskCompletionStatus",
    "TasksTaskInfo",
    "TasksTaskResult",
    "TasksTaskState",
    "TasksTaskTriggerInfo",
    "ThemeMediaResult",
    "TimeSpan",
    "TranscodeReason",
    "TranscodingInfo",
    "TranscodingVpStepInfo",
    "TranscodingVpStepTypes",
    "TupleDoubleDouble",
    "UpdatesInstallationInfo",
    "UpdatesPackageInfo",
    "UpdatesPackageTargetSystem",
    "UpdatesPackageVersionClass",
    "UpdatesPackageVersionInfo",
    "UpdateUserEasyPassword",
    "UpdateUserPassword",
    "UserDto",
    "UserItemDataDto",
    "UserLibraryAddTags",
    "UserLibraryOfficialRatingItem",
    "UserLibraryTagItem",
    "UsersForgotPasswordAction",
    "UsersForgotPasswordResult",
    "UsersPinRedeemResult",
    "UsersUserAction",
    "UsersUserActionType",
    "UsersUserPolicy",
    "ValidatePath",
    "Version",
    "Video3DFormat",
    "VirtualFolderInfo",
    "WakeOnLanInfo",
)
