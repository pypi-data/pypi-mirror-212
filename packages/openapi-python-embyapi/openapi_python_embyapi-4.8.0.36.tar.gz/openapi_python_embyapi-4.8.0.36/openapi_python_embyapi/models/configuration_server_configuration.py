from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.configuration_image_saving_convention import ConfigurationImageSavingConvention
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.configuration_path_substitution import ConfigurationPathSubstitution


T = TypeVar("T", bound="ConfigurationServerConfiguration")


@attr.s(auto_attribs=True)
class ConfigurationServerConfiguration:
    """
    Attributes:
        enable_u_pn_p (Union[Unset, bool]):
        public_port (Union[Unset, int]):
        public_https_port (Union[Unset, int]):
        http_server_port_number (Union[Unset, int]):
        https_port_number (Union[Unset, int]):
        enable_https (Union[Unset, bool]):
        certificate_path (Union[Unset, str]):
        certificate_password (Union[Unset, str]):
        is_port_authorized (Union[Unset, bool]):
        auto_run_web_app (Union[Unset, bool]):
        enable_remote_access (Union[Unset, bool]):
        log_all_query_times (Union[Unset, bool]):
        enable_case_sensitive_item_ids (Union[Unset, bool]):
        metadata_path (Union[Unset, str]):
        metadata_network_path (Union[Unset, str]):
        preferred_metadata_language (Union[Unset, str]):
        metadata_country_code (Union[Unset, str]):
        sort_remove_words (Union[Unset, List[str]]):
        library_monitor_delay (Union[Unset, int]):
        enable_dashboard_response_caching (Union[Unset, bool]):
        dashboard_source_path (Union[Unset, str]):
        image_saving_convention (Union[Unset, ConfigurationImageSavingConvention]):
        enable_automatic_restart (Union[Unset, bool]):
        server_name (Union[Unset, str]):
        wan_ddns (Union[Unset, str]):
        ui_culture (Union[Unset, str]):
        remote_client_bitrate_limit (Union[Unset, int]):
        local_network_subnets (Union[Unset, List[str]]):
        local_network_addresses (Union[Unset, List[str]]):
        enable_external_content_in_suggestions (Union[Unset, bool]):
        require_https (Union[Unset, bool]):
        is_behind_proxy (Union[Unset, bool]):
        remote_ip_filter (Union[Unset, List[str]]):
        is_remote_ip_filter_blacklist (Union[Unset, bool]):
        image_extraction_timeout_ms (Union[Unset, int]):
        path_substitutions (Union[Unset, List['ConfigurationPathSubstitution']]):
        uninstalled_plugins (Union[Unset, List[str]]):
        collapse_video_folders (Union[Unset, bool]):
        enable_original_track_titles (Union[Unset, bool]):
        vacuum_database_on_startup (Union[Unset, bool]):
        simultaneous_stream_limit (Union[Unset, int]):
        database_cache_size_mb (Union[Unset, int]):
        enable_sq_lite_mmio (Union[Unset, bool]):
        channel_options_upgraded (Union[Unset, bool]):
        playlists_upgraded_to_m3u (Union[Unset, bool]):
        timer_ids_upgraded (Union[Unset, bool]):
        forced_sort_name_upgraded (Union[Unset, bool]):
        inherited_parental_rating_value_upgraded (Union[Unset, bool]):
        image_extractor_upgraded (Union[Unset, bool]):
        enable_people_letter_sub_folders (Union[Unset, bool]):
        optimize_database_on_shutdown (Union[Unset, bool]):
        database_analysis_limit (Union[Unset, int]):
        disable_async_io (Union[Unset, bool]):
        migrated_to_user_item_shares (Union[Unset, bool]):
        enable_debug_level_logging (Union[Unset, bool]):
        revert_debug_logging (Union[Unset, str]):
        enable_auto_update (Union[Unset, bool]):
        log_file_retention_days (Union[Unset, int]):
        run_at_startup (Union[Unset, bool]):
        is_startup_wizard_completed (Union[Unset, bool]):
        cache_path (Union[Unset, str]):
    """

    enable_u_pn_p: Union[Unset, bool] = UNSET
    public_port: Union[Unset, int] = UNSET
    public_https_port: Union[Unset, int] = UNSET
    http_server_port_number: Union[Unset, int] = UNSET
    https_port_number: Union[Unset, int] = UNSET
    enable_https: Union[Unset, bool] = UNSET
    certificate_path: Union[Unset, str] = UNSET
    certificate_password: Union[Unset, str] = UNSET
    is_port_authorized: Union[Unset, bool] = UNSET
    auto_run_web_app: Union[Unset, bool] = UNSET
    enable_remote_access: Union[Unset, bool] = UNSET
    log_all_query_times: Union[Unset, bool] = UNSET
    enable_case_sensitive_item_ids: Union[Unset, bool] = UNSET
    metadata_path: Union[Unset, str] = UNSET
    metadata_network_path: Union[Unset, str] = UNSET
    preferred_metadata_language: Union[Unset, str] = UNSET
    metadata_country_code: Union[Unset, str] = UNSET
    sort_remove_words: Union[Unset, List[str]] = UNSET
    library_monitor_delay: Union[Unset, int] = UNSET
    enable_dashboard_response_caching: Union[Unset, bool] = UNSET
    dashboard_source_path: Union[Unset, str] = UNSET
    image_saving_convention: Union[Unset, ConfigurationImageSavingConvention] = UNSET
    enable_automatic_restart: Union[Unset, bool] = UNSET
    server_name: Union[Unset, str] = UNSET
    wan_ddns: Union[Unset, str] = UNSET
    ui_culture: Union[Unset, str] = UNSET
    remote_client_bitrate_limit: Union[Unset, int] = UNSET
    local_network_subnets: Union[Unset, List[str]] = UNSET
    local_network_addresses: Union[Unset, List[str]] = UNSET
    enable_external_content_in_suggestions: Union[Unset, bool] = UNSET
    require_https: Union[Unset, bool] = UNSET
    is_behind_proxy: Union[Unset, bool] = UNSET
    remote_ip_filter: Union[Unset, List[str]] = UNSET
    is_remote_ip_filter_blacklist: Union[Unset, bool] = UNSET
    image_extraction_timeout_ms: Union[Unset, int] = UNSET
    path_substitutions: Union[Unset, List["ConfigurationPathSubstitution"]] = UNSET
    uninstalled_plugins: Union[Unset, List[str]] = UNSET
    collapse_video_folders: Union[Unset, bool] = UNSET
    enable_original_track_titles: Union[Unset, bool] = UNSET
    vacuum_database_on_startup: Union[Unset, bool] = UNSET
    simultaneous_stream_limit: Union[Unset, int] = UNSET
    database_cache_size_mb: Union[Unset, int] = UNSET
    enable_sq_lite_mmio: Union[Unset, bool] = UNSET
    channel_options_upgraded: Union[Unset, bool] = UNSET
    playlists_upgraded_to_m3u: Union[Unset, bool] = UNSET
    timer_ids_upgraded: Union[Unset, bool] = UNSET
    forced_sort_name_upgraded: Union[Unset, bool] = UNSET
    inherited_parental_rating_value_upgraded: Union[Unset, bool] = UNSET
    image_extractor_upgraded: Union[Unset, bool] = UNSET
    enable_people_letter_sub_folders: Union[Unset, bool] = UNSET
    optimize_database_on_shutdown: Union[Unset, bool] = UNSET
    database_analysis_limit: Union[Unset, int] = UNSET
    disable_async_io: Union[Unset, bool] = UNSET
    migrated_to_user_item_shares: Union[Unset, bool] = UNSET
    enable_debug_level_logging: Union[Unset, bool] = UNSET
    revert_debug_logging: Union[Unset, str] = UNSET
    enable_auto_update: Union[Unset, bool] = UNSET
    log_file_retention_days: Union[Unset, int] = UNSET
    run_at_startup: Union[Unset, bool] = UNSET
    is_startup_wizard_completed: Union[Unset, bool] = UNSET
    cache_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enable_u_pn_p = self.enable_u_pn_p
        public_port = self.public_port
        public_https_port = self.public_https_port
        http_server_port_number = self.http_server_port_number
        https_port_number = self.https_port_number
        enable_https = self.enable_https
        certificate_path = self.certificate_path
        certificate_password = self.certificate_password
        is_port_authorized = self.is_port_authorized
        auto_run_web_app = self.auto_run_web_app
        enable_remote_access = self.enable_remote_access
        log_all_query_times = self.log_all_query_times
        enable_case_sensitive_item_ids = self.enable_case_sensitive_item_ids
        metadata_path = self.metadata_path
        metadata_network_path = self.metadata_network_path
        preferred_metadata_language = self.preferred_metadata_language
        metadata_country_code = self.metadata_country_code
        sort_remove_words: Union[Unset, List[str]] = UNSET
        if not isinstance(self.sort_remove_words, Unset):
            sort_remove_words = self.sort_remove_words

        library_monitor_delay = self.library_monitor_delay
        enable_dashboard_response_caching = self.enable_dashboard_response_caching
        dashboard_source_path = self.dashboard_source_path
        image_saving_convention: Union[Unset, str] = UNSET
        if not isinstance(self.image_saving_convention, Unset):
            image_saving_convention = self.image_saving_convention.value

        enable_automatic_restart = self.enable_automatic_restart
        server_name = self.server_name
        wan_ddns = self.wan_ddns
        ui_culture = self.ui_culture
        remote_client_bitrate_limit = self.remote_client_bitrate_limit
        local_network_subnets: Union[Unset, List[str]] = UNSET
        if not isinstance(self.local_network_subnets, Unset):
            local_network_subnets = self.local_network_subnets

        local_network_addresses: Union[Unset, List[str]] = UNSET
        if not isinstance(self.local_network_addresses, Unset):
            local_network_addresses = self.local_network_addresses

        enable_external_content_in_suggestions = self.enable_external_content_in_suggestions
        require_https = self.require_https
        is_behind_proxy = self.is_behind_proxy
        remote_ip_filter: Union[Unset, List[str]] = UNSET
        if not isinstance(self.remote_ip_filter, Unset):
            remote_ip_filter = self.remote_ip_filter

        is_remote_ip_filter_blacklist = self.is_remote_ip_filter_blacklist
        image_extraction_timeout_ms = self.image_extraction_timeout_ms
        path_substitutions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.path_substitutions, Unset):
            path_substitutions = []
            for path_substitutions_item_data in self.path_substitutions:
                path_substitutions_item = path_substitutions_item_data.to_dict()

                path_substitutions.append(path_substitutions_item)

        uninstalled_plugins: Union[Unset, List[str]] = UNSET
        if not isinstance(self.uninstalled_plugins, Unset):
            uninstalled_plugins = self.uninstalled_plugins

        collapse_video_folders = self.collapse_video_folders
        enable_original_track_titles = self.enable_original_track_titles
        vacuum_database_on_startup = self.vacuum_database_on_startup
        simultaneous_stream_limit = self.simultaneous_stream_limit
        database_cache_size_mb = self.database_cache_size_mb
        enable_sq_lite_mmio = self.enable_sq_lite_mmio
        channel_options_upgraded = self.channel_options_upgraded
        playlists_upgraded_to_m3u = self.playlists_upgraded_to_m3u
        timer_ids_upgraded = self.timer_ids_upgraded
        forced_sort_name_upgraded = self.forced_sort_name_upgraded
        inherited_parental_rating_value_upgraded = self.inherited_parental_rating_value_upgraded
        image_extractor_upgraded = self.image_extractor_upgraded
        enable_people_letter_sub_folders = self.enable_people_letter_sub_folders
        optimize_database_on_shutdown = self.optimize_database_on_shutdown
        database_analysis_limit = self.database_analysis_limit
        disable_async_io = self.disable_async_io
        migrated_to_user_item_shares = self.migrated_to_user_item_shares
        enable_debug_level_logging = self.enable_debug_level_logging
        revert_debug_logging = self.revert_debug_logging
        enable_auto_update = self.enable_auto_update
        log_file_retention_days = self.log_file_retention_days
        run_at_startup = self.run_at_startup
        is_startup_wizard_completed = self.is_startup_wizard_completed
        cache_path = self.cache_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enable_u_pn_p is not UNSET:
            field_dict["EnableUPnP"] = enable_u_pn_p
        if public_port is not UNSET:
            field_dict["PublicPort"] = public_port
        if public_https_port is not UNSET:
            field_dict["PublicHttpsPort"] = public_https_port
        if http_server_port_number is not UNSET:
            field_dict["HttpServerPortNumber"] = http_server_port_number
        if https_port_number is not UNSET:
            field_dict["HttpsPortNumber"] = https_port_number
        if enable_https is not UNSET:
            field_dict["EnableHttps"] = enable_https
        if certificate_path is not UNSET:
            field_dict["CertificatePath"] = certificate_path
        if certificate_password is not UNSET:
            field_dict["CertificatePassword"] = certificate_password
        if is_port_authorized is not UNSET:
            field_dict["IsPortAuthorized"] = is_port_authorized
        if auto_run_web_app is not UNSET:
            field_dict["AutoRunWebApp"] = auto_run_web_app
        if enable_remote_access is not UNSET:
            field_dict["EnableRemoteAccess"] = enable_remote_access
        if log_all_query_times is not UNSET:
            field_dict["LogAllQueryTimes"] = log_all_query_times
        if enable_case_sensitive_item_ids is not UNSET:
            field_dict["EnableCaseSensitiveItemIds"] = enable_case_sensitive_item_ids
        if metadata_path is not UNSET:
            field_dict["MetadataPath"] = metadata_path
        if metadata_network_path is not UNSET:
            field_dict["MetadataNetworkPath"] = metadata_network_path
        if preferred_metadata_language is not UNSET:
            field_dict["PreferredMetadataLanguage"] = preferred_metadata_language
        if metadata_country_code is not UNSET:
            field_dict["MetadataCountryCode"] = metadata_country_code
        if sort_remove_words is not UNSET:
            field_dict["SortRemoveWords"] = sort_remove_words
        if library_monitor_delay is not UNSET:
            field_dict["LibraryMonitorDelay"] = library_monitor_delay
        if enable_dashboard_response_caching is not UNSET:
            field_dict["EnableDashboardResponseCaching"] = enable_dashboard_response_caching
        if dashboard_source_path is not UNSET:
            field_dict["DashboardSourcePath"] = dashboard_source_path
        if image_saving_convention is not UNSET:
            field_dict["ImageSavingConvention"] = image_saving_convention
        if enable_automatic_restart is not UNSET:
            field_dict["EnableAutomaticRestart"] = enable_automatic_restart
        if server_name is not UNSET:
            field_dict["ServerName"] = server_name
        if wan_ddns is not UNSET:
            field_dict["WanDdns"] = wan_ddns
        if ui_culture is not UNSET:
            field_dict["UICulture"] = ui_culture
        if remote_client_bitrate_limit is not UNSET:
            field_dict["RemoteClientBitrateLimit"] = remote_client_bitrate_limit
        if local_network_subnets is not UNSET:
            field_dict["LocalNetworkSubnets"] = local_network_subnets
        if local_network_addresses is not UNSET:
            field_dict["LocalNetworkAddresses"] = local_network_addresses
        if enable_external_content_in_suggestions is not UNSET:
            field_dict["EnableExternalContentInSuggestions"] = enable_external_content_in_suggestions
        if require_https is not UNSET:
            field_dict["RequireHttps"] = require_https
        if is_behind_proxy is not UNSET:
            field_dict["IsBehindProxy"] = is_behind_proxy
        if remote_ip_filter is not UNSET:
            field_dict["RemoteIPFilter"] = remote_ip_filter
        if is_remote_ip_filter_blacklist is not UNSET:
            field_dict["IsRemoteIPFilterBlacklist"] = is_remote_ip_filter_blacklist
        if image_extraction_timeout_ms is not UNSET:
            field_dict["ImageExtractionTimeoutMs"] = image_extraction_timeout_ms
        if path_substitutions is not UNSET:
            field_dict["PathSubstitutions"] = path_substitutions
        if uninstalled_plugins is not UNSET:
            field_dict["UninstalledPlugins"] = uninstalled_plugins
        if collapse_video_folders is not UNSET:
            field_dict["CollapseVideoFolders"] = collapse_video_folders
        if enable_original_track_titles is not UNSET:
            field_dict["EnableOriginalTrackTitles"] = enable_original_track_titles
        if vacuum_database_on_startup is not UNSET:
            field_dict["VacuumDatabaseOnStartup"] = vacuum_database_on_startup
        if simultaneous_stream_limit is not UNSET:
            field_dict["SimultaneousStreamLimit"] = simultaneous_stream_limit
        if database_cache_size_mb is not UNSET:
            field_dict["DatabaseCacheSizeMB"] = database_cache_size_mb
        if enable_sq_lite_mmio is not UNSET:
            field_dict["EnableSqLiteMmio"] = enable_sq_lite_mmio
        if channel_options_upgraded is not UNSET:
            field_dict["ChannelOptionsUpgraded"] = channel_options_upgraded
        if playlists_upgraded_to_m3u is not UNSET:
            field_dict["PlaylistsUpgradedToM3U"] = playlists_upgraded_to_m3u
        if timer_ids_upgraded is not UNSET:
            field_dict["TimerIdsUpgraded"] = timer_ids_upgraded
        if forced_sort_name_upgraded is not UNSET:
            field_dict["ForcedSortNameUpgraded"] = forced_sort_name_upgraded
        if inherited_parental_rating_value_upgraded is not UNSET:
            field_dict["InheritedParentalRatingValueUpgraded"] = inherited_parental_rating_value_upgraded
        if image_extractor_upgraded is not UNSET:
            field_dict["ImageExtractorUpgraded"] = image_extractor_upgraded
        if enable_people_letter_sub_folders is not UNSET:
            field_dict["EnablePeopleLetterSubFolders"] = enable_people_letter_sub_folders
        if optimize_database_on_shutdown is not UNSET:
            field_dict["OptimizeDatabaseOnShutdown"] = optimize_database_on_shutdown
        if database_analysis_limit is not UNSET:
            field_dict["DatabaseAnalysisLimit"] = database_analysis_limit
        if disable_async_io is not UNSET:
            field_dict["DisableAsyncIO"] = disable_async_io
        if migrated_to_user_item_shares is not UNSET:
            field_dict["MigratedToUserItemShares"] = migrated_to_user_item_shares
        if enable_debug_level_logging is not UNSET:
            field_dict["EnableDebugLevelLogging"] = enable_debug_level_logging
        if revert_debug_logging is not UNSET:
            field_dict["RevertDebugLogging"] = revert_debug_logging
        if enable_auto_update is not UNSET:
            field_dict["EnableAutoUpdate"] = enable_auto_update
        if log_file_retention_days is not UNSET:
            field_dict["LogFileRetentionDays"] = log_file_retention_days
        if run_at_startup is not UNSET:
            field_dict["RunAtStartup"] = run_at_startup
        if is_startup_wizard_completed is not UNSET:
            field_dict["IsStartupWizardCompleted"] = is_startup_wizard_completed
        if cache_path is not UNSET:
            field_dict["CachePath"] = cache_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.configuration_path_substitution import ConfigurationPathSubstitution

        d = src_dict.copy()
        enable_u_pn_p = d.pop("EnableUPnP", UNSET)

        public_port = d.pop("PublicPort", UNSET)

        public_https_port = d.pop("PublicHttpsPort", UNSET)

        http_server_port_number = d.pop("HttpServerPortNumber", UNSET)

        https_port_number = d.pop("HttpsPortNumber", UNSET)

        enable_https = d.pop("EnableHttps", UNSET)

        certificate_path = d.pop("CertificatePath", UNSET)

        certificate_password = d.pop("CertificatePassword", UNSET)

        is_port_authorized = d.pop("IsPortAuthorized", UNSET)

        auto_run_web_app = d.pop("AutoRunWebApp", UNSET)

        enable_remote_access = d.pop("EnableRemoteAccess", UNSET)

        log_all_query_times = d.pop("LogAllQueryTimes", UNSET)

        enable_case_sensitive_item_ids = d.pop("EnableCaseSensitiveItemIds", UNSET)

        metadata_path = d.pop("MetadataPath", UNSET)

        metadata_network_path = d.pop("MetadataNetworkPath", UNSET)

        preferred_metadata_language = d.pop("PreferredMetadataLanguage", UNSET)

        metadata_country_code = d.pop("MetadataCountryCode", UNSET)

        sort_remove_words = cast(List[str], d.pop("SortRemoveWords", UNSET))

        library_monitor_delay = d.pop("LibraryMonitorDelay", UNSET)

        enable_dashboard_response_caching = d.pop("EnableDashboardResponseCaching", UNSET)

        dashboard_source_path = d.pop("DashboardSourcePath", UNSET)

        _image_saving_convention = d.pop("ImageSavingConvention", UNSET)
        image_saving_convention: Union[Unset, ConfigurationImageSavingConvention]
        if isinstance(_image_saving_convention, Unset):
            image_saving_convention = UNSET
        else:
            image_saving_convention = ConfigurationImageSavingConvention(_image_saving_convention)

        enable_automatic_restart = d.pop("EnableAutomaticRestart", UNSET)

        server_name = d.pop("ServerName", UNSET)

        wan_ddns = d.pop("WanDdns", UNSET)

        ui_culture = d.pop("UICulture", UNSET)

        remote_client_bitrate_limit = d.pop("RemoteClientBitrateLimit", UNSET)

        local_network_subnets = cast(List[str], d.pop("LocalNetworkSubnets", UNSET))

        local_network_addresses = cast(List[str], d.pop("LocalNetworkAddresses", UNSET))

        enable_external_content_in_suggestions = d.pop("EnableExternalContentInSuggestions", UNSET)

        require_https = d.pop("RequireHttps", UNSET)

        is_behind_proxy = d.pop("IsBehindProxy", UNSET)

        remote_ip_filter = cast(List[str], d.pop("RemoteIPFilter", UNSET))

        is_remote_ip_filter_blacklist = d.pop("IsRemoteIPFilterBlacklist", UNSET)

        image_extraction_timeout_ms = d.pop("ImageExtractionTimeoutMs", UNSET)

        path_substitutions = []
        _path_substitutions = d.pop("PathSubstitutions", UNSET)
        for path_substitutions_item_data in _path_substitutions or []:
            path_substitutions_item = ConfigurationPathSubstitution.from_dict(path_substitutions_item_data)

            path_substitutions.append(path_substitutions_item)

        uninstalled_plugins = cast(List[str], d.pop("UninstalledPlugins", UNSET))

        collapse_video_folders = d.pop("CollapseVideoFolders", UNSET)

        enable_original_track_titles = d.pop("EnableOriginalTrackTitles", UNSET)

        vacuum_database_on_startup = d.pop("VacuumDatabaseOnStartup", UNSET)

        simultaneous_stream_limit = d.pop("SimultaneousStreamLimit", UNSET)

        database_cache_size_mb = d.pop("DatabaseCacheSizeMB", UNSET)

        enable_sq_lite_mmio = d.pop("EnableSqLiteMmio", UNSET)

        channel_options_upgraded = d.pop("ChannelOptionsUpgraded", UNSET)

        playlists_upgraded_to_m3u = d.pop("PlaylistsUpgradedToM3U", UNSET)

        timer_ids_upgraded = d.pop("TimerIdsUpgraded", UNSET)

        forced_sort_name_upgraded = d.pop("ForcedSortNameUpgraded", UNSET)

        inherited_parental_rating_value_upgraded = d.pop("InheritedParentalRatingValueUpgraded", UNSET)

        image_extractor_upgraded = d.pop("ImageExtractorUpgraded", UNSET)

        enable_people_letter_sub_folders = d.pop("EnablePeopleLetterSubFolders", UNSET)

        optimize_database_on_shutdown = d.pop("OptimizeDatabaseOnShutdown", UNSET)

        database_analysis_limit = d.pop("DatabaseAnalysisLimit", UNSET)

        disable_async_io = d.pop("DisableAsyncIO", UNSET)

        migrated_to_user_item_shares = d.pop("MigratedToUserItemShares", UNSET)

        enable_debug_level_logging = d.pop("EnableDebugLevelLogging", UNSET)

        revert_debug_logging = d.pop("RevertDebugLogging", UNSET)

        enable_auto_update = d.pop("EnableAutoUpdate", UNSET)

        log_file_retention_days = d.pop("LogFileRetentionDays", UNSET)

        run_at_startup = d.pop("RunAtStartup", UNSET)

        is_startup_wizard_completed = d.pop("IsStartupWizardCompleted", UNSET)

        cache_path = d.pop("CachePath", UNSET)

        configuration_server_configuration = cls(
            enable_u_pn_p=enable_u_pn_p,
            public_port=public_port,
            public_https_port=public_https_port,
            http_server_port_number=http_server_port_number,
            https_port_number=https_port_number,
            enable_https=enable_https,
            certificate_path=certificate_path,
            certificate_password=certificate_password,
            is_port_authorized=is_port_authorized,
            auto_run_web_app=auto_run_web_app,
            enable_remote_access=enable_remote_access,
            log_all_query_times=log_all_query_times,
            enable_case_sensitive_item_ids=enable_case_sensitive_item_ids,
            metadata_path=metadata_path,
            metadata_network_path=metadata_network_path,
            preferred_metadata_language=preferred_metadata_language,
            metadata_country_code=metadata_country_code,
            sort_remove_words=sort_remove_words,
            library_monitor_delay=library_monitor_delay,
            enable_dashboard_response_caching=enable_dashboard_response_caching,
            dashboard_source_path=dashboard_source_path,
            image_saving_convention=image_saving_convention,
            enable_automatic_restart=enable_automatic_restart,
            server_name=server_name,
            wan_ddns=wan_ddns,
            ui_culture=ui_culture,
            remote_client_bitrate_limit=remote_client_bitrate_limit,
            local_network_subnets=local_network_subnets,
            local_network_addresses=local_network_addresses,
            enable_external_content_in_suggestions=enable_external_content_in_suggestions,
            require_https=require_https,
            is_behind_proxy=is_behind_proxy,
            remote_ip_filter=remote_ip_filter,
            is_remote_ip_filter_blacklist=is_remote_ip_filter_blacklist,
            image_extraction_timeout_ms=image_extraction_timeout_ms,
            path_substitutions=path_substitutions,
            uninstalled_plugins=uninstalled_plugins,
            collapse_video_folders=collapse_video_folders,
            enable_original_track_titles=enable_original_track_titles,
            vacuum_database_on_startup=vacuum_database_on_startup,
            simultaneous_stream_limit=simultaneous_stream_limit,
            database_cache_size_mb=database_cache_size_mb,
            enable_sq_lite_mmio=enable_sq_lite_mmio,
            channel_options_upgraded=channel_options_upgraded,
            playlists_upgraded_to_m3u=playlists_upgraded_to_m3u,
            timer_ids_upgraded=timer_ids_upgraded,
            forced_sort_name_upgraded=forced_sort_name_upgraded,
            inherited_parental_rating_value_upgraded=inherited_parental_rating_value_upgraded,
            image_extractor_upgraded=image_extractor_upgraded,
            enable_people_letter_sub_folders=enable_people_letter_sub_folders,
            optimize_database_on_shutdown=optimize_database_on_shutdown,
            database_analysis_limit=database_analysis_limit,
            disable_async_io=disable_async_io,
            migrated_to_user_item_shares=migrated_to_user_item_shares,
            enable_debug_level_logging=enable_debug_level_logging,
            revert_debug_logging=revert_debug_logging,
            enable_auto_update=enable_auto_update,
            log_file_retention_days=log_file_retention_days,
            run_at_startup=run_at_startup,
            is_startup_wizard_completed=is_startup_wizard_completed,
            cache_path=cache_path,
        )

        configuration_server_configuration.additional_properties = d
        return configuration_server_configuration

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
