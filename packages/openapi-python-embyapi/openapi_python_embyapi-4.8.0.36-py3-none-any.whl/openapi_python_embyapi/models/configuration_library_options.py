from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.configuration_media_path_info import ConfigurationMediaPathInfo
    from ..models.configuration_type_options import ConfigurationTypeOptions


T = TypeVar("T", bound="ConfigurationLibraryOptions")


@attr.s(auto_attribs=True)
class ConfigurationLibraryOptions:
    """
    Attributes:
        enable_archive_media_files (Union[Unset, bool]):
        enable_photos (Union[Unset, bool]):
        enable_realtime_monitor (Union[Unset, bool]):
        enable_marker_detection (Union[Unset, bool]):
        enable_marker_detection_during_library_scan (Union[Unset, bool]):
        intro_detection_fingerprint_length (Union[Unset, int]):
        enable_chapter_image_extraction (Union[Unset, bool]):
        extract_chapter_images_during_library_scan (Union[Unset, bool]):
        download_images_in_advance (Union[Unset, bool]):
        path_infos (Union[Unset, List['ConfigurationMediaPathInfo']]):
        ignore_hidden_files (Union[Unset, bool]):
        ignore_file_extensions (Union[Unset, List[str]]):
        save_local_metadata (Union[Unset, bool]):
        save_metadata_hidden (Union[Unset, bool]):
        save_local_thumbnail_sets (Union[Unset, bool]):
        import_missing_episodes (Union[Unset, bool]):
        import_playlists (Union[Unset, bool]):
        enable_automatic_series_grouping (Union[Unset, bool]):
        enable_embedded_titles (Union[Unset, bool]):
        enable_audio_resume (Union[Unset, bool]):
        automatic_refresh_interval_days (Union[Unset, int]):
        placeholder_metadata_refresh_interval_days (Union[Unset, int]):
        preferred_metadata_language (Union[Unset, str]):
        preferred_image_language (Union[Unset, str]):
        content_type (Union[Unset, str]):
        metadata_country_code (Union[Unset, str]):
        season_zero_display_name (Union[Unset, str]):
        name (Union[Unset, str]):
        metadata_savers (Union[Unset, List[str]]):
        disabled_local_metadata_readers (Union[Unset, List[str]]):
        local_metadata_reader_order (Union[Unset, List[str]]):
        disabled_lyrics_fetchers (Union[Unset, List[str]]):
        save_lyrics_with_media (Union[Unset, bool]):
        lyrics_download_max_age_days (Union[Unset, int]):
        lyrics_fetcher_order (Union[Unset, List[str]]):
        lyrics_download_languages (Union[Unset, List[str]]):
        disabled_subtitle_fetchers (Union[Unset, List[str]]):
        subtitle_fetcher_order (Union[Unset, List[str]]):
        skip_subtitles_if_embedded_subtitles_present (Union[Unset, bool]):
        skip_subtitles_if_audio_track_matches (Union[Unset, bool]):
        subtitle_download_languages (Union[Unset, List[str]]):
        subtitle_download_max_age_days (Union[Unset, int]):
        require_perfect_subtitle_match (Union[Unset, bool]):
        save_subtitles_with_media (Union[Unset, bool]):
        forced_subtitles_only (Union[Unset, bool]):
        type_options (Union[Unset, List['ConfigurationTypeOptions']]):
        collapse_single_item_folders (Union[Unset, bool]):
        enable_adult_metadata (Union[Unset, bool]):
        import_collections (Union[Unset, bool]):
        min_collection_items (Union[Unset, int]):
        music_folder_structure (Union[Unset, str]):
        min_resume_pct (Union[Unset, int]):
        max_resume_pct (Union[Unset, int]):
        min_resume_duration_seconds (Union[Unset, int]):
        thumbnail_images_interval_seconds (Union[Unset, int]):
        sample_ignore_size (Union[Unset, int]):
    """

    enable_archive_media_files: Union[Unset, bool] = UNSET
    enable_photos: Union[Unset, bool] = UNSET
    enable_realtime_monitor: Union[Unset, bool] = UNSET
    enable_marker_detection: Union[Unset, bool] = UNSET
    enable_marker_detection_during_library_scan: Union[Unset, bool] = UNSET
    intro_detection_fingerprint_length: Union[Unset, int] = UNSET
    enable_chapter_image_extraction: Union[Unset, bool] = UNSET
    extract_chapter_images_during_library_scan: Union[Unset, bool] = UNSET
    download_images_in_advance: Union[Unset, bool] = UNSET
    path_infos: Union[Unset, List["ConfigurationMediaPathInfo"]] = UNSET
    ignore_hidden_files: Union[Unset, bool] = UNSET
    ignore_file_extensions: Union[Unset, List[str]] = UNSET
    save_local_metadata: Union[Unset, bool] = UNSET
    save_metadata_hidden: Union[Unset, bool] = UNSET
    save_local_thumbnail_sets: Union[Unset, bool] = UNSET
    import_missing_episodes: Union[Unset, bool] = UNSET
    import_playlists: Union[Unset, bool] = UNSET
    enable_automatic_series_grouping: Union[Unset, bool] = UNSET
    enable_embedded_titles: Union[Unset, bool] = UNSET
    enable_audio_resume: Union[Unset, bool] = UNSET
    automatic_refresh_interval_days: Union[Unset, int] = UNSET
    placeholder_metadata_refresh_interval_days: Union[Unset, int] = UNSET
    preferred_metadata_language: Union[Unset, str] = UNSET
    preferred_image_language: Union[Unset, str] = UNSET
    content_type: Union[Unset, str] = UNSET
    metadata_country_code: Union[Unset, str] = UNSET
    season_zero_display_name: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    metadata_savers: Union[Unset, List[str]] = UNSET
    disabled_local_metadata_readers: Union[Unset, List[str]] = UNSET
    local_metadata_reader_order: Union[Unset, List[str]] = UNSET
    disabled_lyrics_fetchers: Union[Unset, List[str]] = UNSET
    save_lyrics_with_media: Union[Unset, bool] = UNSET
    lyrics_download_max_age_days: Union[Unset, int] = UNSET
    lyrics_fetcher_order: Union[Unset, List[str]] = UNSET
    lyrics_download_languages: Union[Unset, List[str]] = UNSET
    disabled_subtitle_fetchers: Union[Unset, List[str]] = UNSET
    subtitle_fetcher_order: Union[Unset, List[str]] = UNSET
    skip_subtitles_if_embedded_subtitles_present: Union[Unset, bool] = UNSET
    skip_subtitles_if_audio_track_matches: Union[Unset, bool] = UNSET
    subtitle_download_languages: Union[Unset, List[str]] = UNSET
    subtitle_download_max_age_days: Union[Unset, int] = UNSET
    require_perfect_subtitle_match: Union[Unset, bool] = UNSET
    save_subtitles_with_media: Union[Unset, bool] = UNSET
    forced_subtitles_only: Union[Unset, bool] = UNSET
    type_options: Union[Unset, List["ConfigurationTypeOptions"]] = UNSET
    collapse_single_item_folders: Union[Unset, bool] = UNSET
    enable_adult_metadata: Union[Unset, bool] = UNSET
    import_collections: Union[Unset, bool] = UNSET
    min_collection_items: Union[Unset, int] = UNSET
    music_folder_structure: Union[Unset, str] = UNSET
    min_resume_pct: Union[Unset, int] = UNSET
    max_resume_pct: Union[Unset, int] = UNSET
    min_resume_duration_seconds: Union[Unset, int] = UNSET
    thumbnail_images_interval_seconds: Union[Unset, int] = UNSET
    sample_ignore_size: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enable_archive_media_files = self.enable_archive_media_files
        enable_photos = self.enable_photos
        enable_realtime_monitor = self.enable_realtime_monitor
        enable_marker_detection = self.enable_marker_detection
        enable_marker_detection_during_library_scan = self.enable_marker_detection_during_library_scan
        intro_detection_fingerprint_length = self.intro_detection_fingerprint_length
        enable_chapter_image_extraction = self.enable_chapter_image_extraction
        extract_chapter_images_during_library_scan = self.extract_chapter_images_during_library_scan
        download_images_in_advance = self.download_images_in_advance
        path_infos: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.path_infos, Unset):
            path_infos = []
            for path_infos_item_data in self.path_infos:
                path_infos_item = path_infos_item_data.to_dict()

                path_infos.append(path_infos_item)

        ignore_hidden_files = self.ignore_hidden_files
        ignore_file_extensions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.ignore_file_extensions, Unset):
            ignore_file_extensions = self.ignore_file_extensions

        save_local_metadata = self.save_local_metadata
        save_metadata_hidden = self.save_metadata_hidden
        save_local_thumbnail_sets = self.save_local_thumbnail_sets
        import_missing_episodes = self.import_missing_episodes
        import_playlists = self.import_playlists
        enable_automatic_series_grouping = self.enable_automatic_series_grouping
        enable_embedded_titles = self.enable_embedded_titles
        enable_audio_resume = self.enable_audio_resume
        automatic_refresh_interval_days = self.automatic_refresh_interval_days
        placeholder_metadata_refresh_interval_days = self.placeholder_metadata_refresh_interval_days
        preferred_metadata_language = self.preferred_metadata_language
        preferred_image_language = self.preferred_image_language
        content_type = self.content_type
        metadata_country_code = self.metadata_country_code
        season_zero_display_name = self.season_zero_display_name
        name = self.name
        metadata_savers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.metadata_savers, Unset):
            metadata_savers = self.metadata_savers

        disabled_local_metadata_readers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.disabled_local_metadata_readers, Unset):
            disabled_local_metadata_readers = self.disabled_local_metadata_readers

        local_metadata_reader_order: Union[Unset, List[str]] = UNSET
        if not isinstance(self.local_metadata_reader_order, Unset):
            local_metadata_reader_order = self.local_metadata_reader_order

        disabled_lyrics_fetchers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.disabled_lyrics_fetchers, Unset):
            disabled_lyrics_fetchers = self.disabled_lyrics_fetchers

        save_lyrics_with_media = self.save_lyrics_with_media
        lyrics_download_max_age_days = self.lyrics_download_max_age_days
        lyrics_fetcher_order: Union[Unset, List[str]] = UNSET
        if not isinstance(self.lyrics_fetcher_order, Unset):
            lyrics_fetcher_order = self.lyrics_fetcher_order

        lyrics_download_languages: Union[Unset, List[str]] = UNSET
        if not isinstance(self.lyrics_download_languages, Unset):
            lyrics_download_languages = self.lyrics_download_languages

        disabled_subtitle_fetchers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.disabled_subtitle_fetchers, Unset):
            disabled_subtitle_fetchers = self.disabled_subtitle_fetchers

        subtitle_fetcher_order: Union[Unset, List[str]] = UNSET
        if not isinstance(self.subtitle_fetcher_order, Unset):
            subtitle_fetcher_order = self.subtitle_fetcher_order

        skip_subtitles_if_embedded_subtitles_present = self.skip_subtitles_if_embedded_subtitles_present
        skip_subtitles_if_audio_track_matches = self.skip_subtitles_if_audio_track_matches
        subtitle_download_languages: Union[Unset, List[str]] = UNSET
        if not isinstance(self.subtitle_download_languages, Unset):
            subtitle_download_languages = self.subtitle_download_languages

        subtitle_download_max_age_days = self.subtitle_download_max_age_days
        require_perfect_subtitle_match = self.require_perfect_subtitle_match
        save_subtitles_with_media = self.save_subtitles_with_media
        forced_subtitles_only = self.forced_subtitles_only
        type_options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.type_options, Unset):
            type_options = []
            for type_options_item_data in self.type_options:
                type_options_item = type_options_item_data.to_dict()

                type_options.append(type_options_item)

        collapse_single_item_folders = self.collapse_single_item_folders
        enable_adult_metadata = self.enable_adult_metadata
        import_collections = self.import_collections
        min_collection_items = self.min_collection_items
        music_folder_structure = self.music_folder_structure
        min_resume_pct = self.min_resume_pct
        max_resume_pct = self.max_resume_pct
        min_resume_duration_seconds = self.min_resume_duration_seconds
        thumbnail_images_interval_seconds = self.thumbnail_images_interval_seconds
        sample_ignore_size = self.sample_ignore_size

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enable_archive_media_files is not UNSET:
            field_dict["EnableArchiveMediaFiles"] = enable_archive_media_files
        if enable_photos is not UNSET:
            field_dict["EnablePhotos"] = enable_photos
        if enable_realtime_monitor is not UNSET:
            field_dict["EnableRealtimeMonitor"] = enable_realtime_monitor
        if enable_marker_detection is not UNSET:
            field_dict["EnableMarkerDetection"] = enable_marker_detection
        if enable_marker_detection_during_library_scan is not UNSET:
            field_dict["EnableMarkerDetectionDuringLibraryScan"] = enable_marker_detection_during_library_scan
        if intro_detection_fingerprint_length is not UNSET:
            field_dict["IntroDetectionFingerprintLength"] = intro_detection_fingerprint_length
        if enable_chapter_image_extraction is not UNSET:
            field_dict["EnableChapterImageExtraction"] = enable_chapter_image_extraction
        if extract_chapter_images_during_library_scan is not UNSET:
            field_dict["ExtractChapterImagesDuringLibraryScan"] = extract_chapter_images_during_library_scan
        if download_images_in_advance is not UNSET:
            field_dict["DownloadImagesInAdvance"] = download_images_in_advance
        if path_infos is not UNSET:
            field_dict["PathInfos"] = path_infos
        if ignore_hidden_files is not UNSET:
            field_dict["IgnoreHiddenFiles"] = ignore_hidden_files
        if ignore_file_extensions is not UNSET:
            field_dict["IgnoreFileExtensions"] = ignore_file_extensions
        if save_local_metadata is not UNSET:
            field_dict["SaveLocalMetadata"] = save_local_metadata
        if save_metadata_hidden is not UNSET:
            field_dict["SaveMetadataHidden"] = save_metadata_hidden
        if save_local_thumbnail_sets is not UNSET:
            field_dict["SaveLocalThumbnailSets"] = save_local_thumbnail_sets
        if import_missing_episodes is not UNSET:
            field_dict["ImportMissingEpisodes"] = import_missing_episodes
        if import_playlists is not UNSET:
            field_dict["ImportPlaylists"] = import_playlists
        if enable_automatic_series_grouping is not UNSET:
            field_dict["EnableAutomaticSeriesGrouping"] = enable_automatic_series_grouping
        if enable_embedded_titles is not UNSET:
            field_dict["EnableEmbeddedTitles"] = enable_embedded_titles
        if enable_audio_resume is not UNSET:
            field_dict["EnableAudioResume"] = enable_audio_resume
        if automatic_refresh_interval_days is not UNSET:
            field_dict["AutomaticRefreshIntervalDays"] = automatic_refresh_interval_days
        if placeholder_metadata_refresh_interval_days is not UNSET:
            field_dict["PlaceholderMetadataRefreshIntervalDays"] = placeholder_metadata_refresh_interval_days
        if preferred_metadata_language is not UNSET:
            field_dict["PreferredMetadataLanguage"] = preferred_metadata_language
        if preferred_image_language is not UNSET:
            field_dict["PreferredImageLanguage"] = preferred_image_language
        if content_type is not UNSET:
            field_dict["ContentType"] = content_type
        if metadata_country_code is not UNSET:
            field_dict["MetadataCountryCode"] = metadata_country_code
        if season_zero_display_name is not UNSET:
            field_dict["SeasonZeroDisplayName"] = season_zero_display_name
        if name is not UNSET:
            field_dict["Name"] = name
        if metadata_savers is not UNSET:
            field_dict["MetadataSavers"] = metadata_savers
        if disabled_local_metadata_readers is not UNSET:
            field_dict["DisabledLocalMetadataReaders"] = disabled_local_metadata_readers
        if local_metadata_reader_order is not UNSET:
            field_dict["LocalMetadataReaderOrder"] = local_metadata_reader_order
        if disabled_lyrics_fetchers is not UNSET:
            field_dict["DisabledLyricsFetchers"] = disabled_lyrics_fetchers
        if save_lyrics_with_media is not UNSET:
            field_dict["SaveLyricsWithMedia"] = save_lyrics_with_media
        if lyrics_download_max_age_days is not UNSET:
            field_dict["LyricsDownloadMaxAgeDays"] = lyrics_download_max_age_days
        if lyrics_fetcher_order is not UNSET:
            field_dict["LyricsFetcherOrder"] = lyrics_fetcher_order
        if lyrics_download_languages is not UNSET:
            field_dict["LyricsDownloadLanguages"] = lyrics_download_languages
        if disabled_subtitle_fetchers is not UNSET:
            field_dict["DisabledSubtitleFetchers"] = disabled_subtitle_fetchers
        if subtitle_fetcher_order is not UNSET:
            field_dict["SubtitleFetcherOrder"] = subtitle_fetcher_order
        if skip_subtitles_if_embedded_subtitles_present is not UNSET:
            field_dict["SkipSubtitlesIfEmbeddedSubtitlesPresent"] = skip_subtitles_if_embedded_subtitles_present
        if skip_subtitles_if_audio_track_matches is not UNSET:
            field_dict["SkipSubtitlesIfAudioTrackMatches"] = skip_subtitles_if_audio_track_matches
        if subtitle_download_languages is not UNSET:
            field_dict["SubtitleDownloadLanguages"] = subtitle_download_languages
        if subtitle_download_max_age_days is not UNSET:
            field_dict["SubtitleDownloadMaxAgeDays"] = subtitle_download_max_age_days
        if require_perfect_subtitle_match is not UNSET:
            field_dict["RequirePerfectSubtitleMatch"] = require_perfect_subtitle_match
        if save_subtitles_with_media is not UNSET:
            field_dict["SaveSubtitlesWithMedia"] = save_subtitles_with_media
        if forced_subtitles_only is not UNSET:
            field_dict["ForcedSubtitlesOnly"] = forced_subtitles_only
        if type_options is not UNSET:
            field_dict["TypeOptions"] = type_options
        if collapse_single_item_folders is not UNSET:
            field_dict["CollapseSingleItemFolders"] = collapse_single_item_folders
        if enable_adult_metadata is not UNSET:
            field_dict["EnableAdultMetadata"] = enable_adult_metadata
        if import_collections is not UNSET:
            field_dict["ImportCollections"] = import_collections
        if min_collection_items is not UNSET:
            field_dict["MinCollectionItems"] = min_collection_items
        if music_folder_structure is not UNSET:
            field_dict["MusicFolderStructure"] = music_folder_structure
        if min_resume_pct is not UNSET:
            field_dict["MinResumePct"] = min_resume_pct
        if max_resume_pct is not UNSET:
            field_dict["MaxResumePct"] = max_resume_pct
        if min_resume_duration_seconds is not UNSET:
            field_dict["MinResumeDurationSeconds"] = min_resume_duration_seconds
        if thumbnail_images_interval_seconds is not UNSET:
            field_dict["ThumbnailImagesIntervalSeconds"] = thumbnail_images_interval_seconds
        if sample_ignore_size is not UNSET:
            field_dict["SampleIgnoreSize"] = sample_ignore_size

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.configuration_media_path_info import ConfigurationMediaPathInfo
        from ..models.configuration_type_options import ConfigurationTypeOptions

        d = src_dict.copy()
        enable_archive_media_files = d.pop("EnableArchiveMediaFiles", UNSET)

        enable_photos = d.pop("EnablePhotos", UNSET)

        enable_realtime_monitor = d.pop("EnableRealtimeMonitor", UNSET)

        enable_marker_detection = d.pop("EnableMarkerDetection", UNSET)

        enable_marker_detection_during_library_scan = d.pop("EnableMarkerDetectionDuringLibraryScan", UNSET)

        intro_detection_fingerprint_length = d.pop("IntroDetectionFingerprintLength", UNSET)

        enable_chapter_image_extraction = d.pop("EnableChapterImageExtraction", UNSET)

        extract_chapter_images_during_library_scan = d.pop("ExtractChapterImagesDuringLibraryScan", UNSET)

        download_images_in_advance = d.pop("DownloadImagesInAdvance", UNSET)

        path_infos = []
        _path_infos = d.pop("PathInfos", UNSET)
        for path_infos_item_data in _path_infos or []:
            path_infos_item = ConfigurationMediaPathInfo.from_dict(path_infos_item_data)

            path_infos.append(path_infos_item)

        ignore_hidden_files = d.pop("IgnoreHiddenFiles", UNSET)

        ignore_file_extensions = cast(List[str], d.pop("IgnoreFileExtensions", UNSET))

        save_local_metadata = d.pop("SaveLocalMetadata", UNSET)

        save_metadata_hidden = d.pop("SaveMetadataHidden", UNSET)

        save_local_thumbnail_sets = d.pop("SaveLocalThumbnailSets", UNSET)

        import_missing_episodes = d.pop("ImportMissingEpisodes", UNSET)

        import_playlists = d.pop("ImportPlaylists", UNSET)

        enable_automatic_series_grouping = d.pop("EnableAutomaticSeriesGrouping", UNSET)

        enable_embedded_titles = d.pop("EnableEmbeddedTitles", UNSET)

        enable_audio_resume = d.pop("EnableAudioResume", UNSET)

        automatic_refresh_interval_days = d.pop("AutomaticRefreshIntervalDays", UNSET)

        placeholder_metadata_refresh_interval_days = d.pop("PlaceholderMetadataRefreshIntervalDays", UNSET)

        preferred_metadata_language = d.pop("PreferredMetadataLanguage", UNSET)

        preferred_image_language = d.pop("PreferredImageLanguage", UNSET)

        content_type = d.pop("ContentType", UNSET)

        metadata_country_code = d.pop("MetadataCountryCode", UNSET)

        season_zero_display_name = d.pop("SeasonZeroDisplayName", UNSET)

        name = d.pop("Name", UNSET)

        metadata_savers = cast(List[str], d.pop("MetadataSavers", UNSET))

        disabled_local_metadata_readers = cast(List[str], d.pop("DisabledLocalMetadataReaders", UNSET))

        local_metadata_reader_order = cast(List[str], d.pop("LocalMetadataReaderOrder", UNSET))

        disabled_lyrics_fetchers = cast(List[str], d.pop("DisabledLyricsFetchers", UNSET))

        save_lyrics_with_media = d.pop("SaveLyricsWithMedia", UNSET)

        lyrics_download_max_age_days = d.pop("LyricsDownloadMaxAgeDays", UNSET)

        lyrics_fetcher_order = cast(List[str], d.pop("LyricsFetcherOrder", UNSET))

        lyrics_download_languages = cast(List[str], d.pop("LyricsDownloadLanguages", UNSET))

        disabled_subtitle_fetchers = cast(List[str], d.pop("DisabledSubtitleFetchers", UNSET))

        subtitle_fetcher_order = cast(List[str], d.pop("SubtitleFetcherOrder", UNSET))

        skip_subtitles_if_embedded_subtitles_present = d.pop("SkipSubtitlesIfEmbeddedSubtitlesPresent", UNSET)

        skip_subtitles_if_audio_track_matches = d.pop("SkipSubtitlesIfAudioTrackMatches", UNSET)

        subtitle_download_languages = cast(List[str], d.pop("SubtitleDownloadLanguages", UNSET))

        subtitle_download_max_age_days = d.pop("SubtitleDownloadMaxAgeDays", UNSET)

        require_perfect_subtitle_match = d.pop("RequirePerfectSubtitleMatch", UNSET)

        save_subtitles_with_media = d.pop("SaveSubtitlesWithMedia", UNSET)

        forced_subtitles_only = d.pop("ForcedSubtitlesOnly", UNSET)

        type_options = []
        _type_options = d.pop("TypeOptions", UNSET)
        for type_options_item_data in _type_options or []:
            type_options_item = ConfigurationTypeOptions.from_dict(type_options_item_data)

            type_options.append(type_options_item)

        collapse_single_item_folders = d.pop("CollapseSingleItemFolders", UNSET)

        enable_adult_metadata = d.pop("EnableAdultMetadata", UNSET)

        import_collections = d.pop("ImportCollections", UNSET)

        min_collection_items = d.pop("MinCollectionItems", UNSET)

        music_folder_structure = d.pop("MusicFolderStructure", UNSET)

        min_resume_pct = d.pop("MinResumePct", UNSET)

        max_resume_pct = d.pop("MaxResumePct", UNSET)

        min_resume_duration_seconds = d.pop("MinResumeDurationSeconds", UNSET)

        thumbnail_images_interval_seconds = d.pop("ThumbnailImagesIntervalSeconds", UNSET)

        sample_ignore_size = d.pop("SampleIgnoreSize", UNSET)

        configuration_library_options = cls(
            enable_archive_media_files=enable_archive_media_files,
            enable_photos=enable_photos,
            enable_realtime_monitor=enable_realtime_monitor,
            enable_marker_detection=enable_marker_detection,
            enable_marker_detection_during_library_scan=enable_marker_detection_during_library_scan,
            intro_detection_fingerprint_length=intro_detection_fingerprint_length,
            enable_chapter_image_extraction=enable_chapter_image_extraction,
            extract_chapter_images_during_library_scan=extract_chapter_images_during_library_scan,
            download_images_in_advance=download_images_in_advance,
            path_infos=path_infos,
            ignore_hidden_files=ignore_hidden_files,
            ignore_file_extensions=ignore_file_extensions,
            save_local_metadata=save_local_metadata,
            save_metadata_hidden=save_metadata_hidden,
            save_local_thumbnail_sets=save_local_thumbnail_sets,
            import_missing_episodes=import_missing_episodes,
            import_playlists=import_playlists,
            enable_automatic_series_grouping=enable_automatic_series_grouping,
            enable_embedded_titles=enable_embedded_titles,
            enable_audio_resume=enable_audio_resume,
            automatic_refresh_interval_days=automatic_refresh_interval_days,
            placeholder_metadata_refresh_interval_days=placeholder_metadata_refresh_interval_days,
            preferred_metadata_language=preferred_metadata_language,
            preferred_image_language=preferred_image_language,
            content_type=content_type,
            metadata_country_code=metadata_country_code,
            season_zero_display_name=season_zero_display_name,
            name=name,
            metadata_savers=metadata_savers,
            disabled_local_metadata_readers=disabled_local_metadata_readers,
            local_metadata_reader_order=local_metadata_reader_order,
            disabled_lyrics_fetchers=disabled_lyrics_fetchers,
            save_lyrics_with_media=save_lyrics_with_media,
            lyrics_download_max_age_days=lyrics_download_max_age_days,
            lyrics_fetcher_order=lyrics_fetcher_order,
            lyrics_download_languages=lyrics_download_languages,
            disabled_subtitle_fetchers=disabled_subtitle_fetchers,
            subtitle_fetcher_order=subtitle_fetcher_order,
            skip_subtitles_if_embedded_subtitles_present=skip_subtitles_if_embedded_subtitles_present,
            skip_subtitles_if_audio_track_matches=skip_subtitles_if_audio_track_matches,
            subtitle_download_languages=subtitle_download_languages,
            subtitle_download_max_age_days=subtitle_download_max_age_days,
            require_perfect_subtitle_match=require_perfect_subtitle_match,
            save_subtitles_with_media=save_subtitles_with_media,
            forced_subtitles_only=forced_subtitles_only,
            type_options=type_options,
            collapse_single_item_folders=collapse_single_item_folders,
            enable_adult_metadata=enable_adult_metadata,
            import_collections=import_collections,
            min_collection_items=min_collection_items,
            music_folder_structure=music_folder_structure,
            min_resume_pct=min_resume_pct,
            max_resume_pct=max_resume_pct,
            min_resume_duration_seconds=min_resume_duration_seconds,
            thumbnail_images_interval_seconds=thumbnail_images_interval_seconds,
            sample_ignore_size=sample_ignore_size,
        )

        configuration_library_options.additional_properties = d
        return configuration_library_options

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
