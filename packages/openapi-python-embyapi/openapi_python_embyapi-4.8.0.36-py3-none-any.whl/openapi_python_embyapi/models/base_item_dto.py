import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.day_of_week import DayOfWeek
from ..models.drawing_image_orientation import DrawingImageOrientation
from ..models.live_tv_timer_type import LiveTvTimerType
from ..models.location_type import LocationType
from ..models.metadata_fields import MetadataFields
from ..models.video_3d_format import Video3DFormat
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_item_dto_image_tags import BaseItemDtoImageTags
    from ..models.base_item_person import BaseItemPerson
    from ..models.chapter_info import ChapterInfo
    from ..models.external_url import ExternalUrl
    from ..models.media_source_info import MediaSourceInfo
    from ..models.media_stream import MediaStream
    from ..models.media_url import MediaUrl
    from ..models.name_id_pair import NameIdPair
    from ..models.name_long_id_pair import NameLongIdPair
    from ..models.provider_id_dictionary import ProviderIdDictionary
    from ..models.user_item_data_dto import UserItemDataDto


T = TypeVar("T", bound="BaseItemDto")


@attr.s(auto_attribs=True)
class BaseItemDto:
    """
    Attributes:
        name (Union[Unset, str]):
        original_title (Union[Unset, str]):
        server_id (Union[Unset, str]):
        id (Union[Unset, str]):
        guid (Union[Unset, str]):
        etag (Union[Unset, str]):
        prefix (Union[Unset, str]):
        playlist_item_id (Union[Unset, str]):
        date_created (Union[Unset, None, datetime.datetime]):
        extra_type (Union[Unset, str]):
        sort_index_number (Union[Unset, None, int]):
        sort_parent_index_number (Union[Unset, None, int]):
        can_delete (Union[Unset, None, bool]):
        can_download (Union[Unset, None, bool]):
        supports_resume (Union[Unset, None, bool]):
        presentation_unique_key (Union[Unset, str]):
        preferred_metadata_language (Union[Unset, str]):
        preferred_metadata_country_code (Union[Unset, str]):
        supports_sync (Union[Unset, None, bool]):
        can_manage_access (Union[Unset, None, bool]):
        can_make_private (Union[Unset, None, bool]):
        can_make_public (Union[Unset, None, bool]):
        container (Union[Unset, str]):
        sort_name (Union[Unset, str]):
        forced_sort_name (Union[Unset, str]):
        video_3d_format (Union[Unset, Video3DFormat]):
        premiere_date (Union[Unset, None, datetime.datetime]):
        external_urls (Union[Unset, List['ExternalUrl']]):
        media_sources (Union[Unset, List['MediaSourceInfo']]):
        critic_rating (Union[Unset, None, float]):
        game_system_id (Union[Unset, None, int]):
        as_series (Union[Unset, None, bool]):
        game_system (Union[Unset, str]):
        production_locations (Union[Unset, List[str]]):
        path (Union[Unset, str]):
        official_rating (Union[Unset, str]):
        custom_rating (Union[Unset, str]):
        channel_id (Union[Unset, str]):
        channel_name (Union[Unset, str]):
        overview (Union[Unset, str]):
        taglines (Union[Unset, List[str]]):
        genres (Union[Unset, List[str]]):
        community_rating (Union[Unset, None, float]):
        run_time_ticks (Union[Unset, None, int]):
        size (Union[Unset, None, int]):
        file_name (Union[Unset, str]):
        bitrate (Union[Unset, None, int]):
        production_year (Union[Unset, None, int]):
        number (Union[Unset, str]):
        channel_number (Union[Unset, str]):
        index_number (Union[Unset, None, int]):
        index_number_end (Union[Unset, None, int]):
        parent_index_number (Union[Unset, None, int]):
        remote_trailers (Union[Unset, List['MediaUrl']]):
        provider_ids (Union[Unset, ProviderIdDictionary]):
        is_folder (Union[Unset, None, bool]):
        parent_id (Union[Unset, str]):
        type (Union[Unset, str]):
        people (Union[Unset, List['BaseItemPerson']]):
        studios (Union[Unset, List['NameLongIdPair']]):
        genre_items (Union[Unset, List['NameLongIdPair']]):
        tag_items (Union[Unset, List['NameLongIdPair']]):
        parent_logo_item_id (Union[Unset, str]):
        parent_backdrop_item_id (Union[Unset, str]):
        parent_backdrop_image_tags (Union[Unset, List[str]]):
        local_trailer_count (Union[Unset, None, int]):
        user_data (Union[Unset, UserItemDataDto]):
        recursive_item_count (Union[Unset, None, int]):
        child_count (Union[Unset, None, int]):
        series_name (Union[Unset, str]):
        series_id (Union[Unset, str]):
        season_id (Union[Unset, str]):
        special_feature_count (Union[Unset, None, int]):
        display_preferences_id (Union[Unset, str]):
        status (Union[Unset, str]):
        air_days (Union[Unset, List[DayOfWeek]]):
        tags (Union[Unset, List[str]]):
        primary_image_aspect_ratio (Union[Unset, None, float]):
        artists (Union[Unset, List[str]]):
        artist_items (Union[Unset, List['NameIdPair']]):
        composers (Union[Unset, List['NameIdPair']]):
        album (Union[Unset, str]):
        collection_type (Union[Unset, str]):
        display_order (Union[Unset, str]):
        album_id (Union[Unset, str]):
        album_primary_image_tag (Union[Unset, str]):
        series_primary_image_tag (Union[Unset, str]):
        album_artist (Union[Unset, str]):
        album_artists (Union[Unset, List['NameIdPair']]):
        season_name (Union[Unset, str]):
        media_streams (Union[Unset, List['MediaStream']]):
        part_count (Union[Unset, None, int]):
        image_tags (Union[Unset, BaseItemDtoImageTags]):
        backdrop_image_tags (Union[Unset, List[str]]):
        parent_logo_image_tag (Union[Unset, str]):
        series_studio (Union[Unset, str]):
        parent_thumb_item_id (Union[Unset, str]):
        parent_thumb_image_tag (Union[Unset, str]):
        chapters (Union[Unset, List['ChapterInfo']]):
        location_type (Union[Unset, LocationType]):
        media_type (Union[Unset, str]):
        end_date (Union[Unset, None, datetime.datetime]):
        locked_fields (Union[Unset, List[MetadataFields]]):
        lock_data (Union[Unset, None, bool]):
        width (Union[Unset, None, int]):
        height (Union[Unset, None, int]):
        camera_make (Union[Unset, str]):
        camera_model (Union[Unset, str]):
        software (Union[Unset, str]):
        exposure_time (Union[Unset, None, float]):
        focal_length (Union[Unset, None, float]):
        image_orientation (Union[Unset, DrawingImageOrientation]):
        aperture (Union[Unset, None, float]):
        shutter_speed (Union[Unset, None, float]):
        latitude (Union[Unset, None, float]):
        longitude (Union[Unset, None, float]):
        altitude (Union[Unset, None, float]):
        iso_speed_rating (Union[Unset, None, int]):
        series_timer_id (Union[Unset, str]):
        channel_primary_image_tag (Union[Unset, str]):
        start_date (Union[Unset, None, datetime.datetime]):
        completion_percentage (Union[Unset, None, float]):
        is_repeat (Union[Unset, None, bool]):
        is_new (Union[Unset, None, bool]):
        episode_title (Union[Unset, str]):
        is_movie (Union[Unset, None, bool]):
        is_sports (Union[Unset, None, bool]):
        is_series (Union[Unset, None, bool]):
        is_live (Union[Unset, None, bool]):
        is_news (Union[Unset, None, bool]):
        is_kids (Union[Unset, None, bool]):
        is_premiere (Union[Unset, None, bool]):
        timer_type (Union[Unset, LiveTvTimerType]):
        disabled (Union[Unset, None, bool]):
        management_id (Union[Unset, str]):
        timer_id (Union[Unset, str]):
        current_program (Union[Unset, BaseItemDto]):
        movie_count (Union[Unset, None, int]):
        series_count (Union[Unset, None, int]):
        album_count (Union[Unset, None, int]):
        song_count (Union[Unset, None, int]):
        music_video_count (Union[Unset, None, int]):
        subviews (Union[Unset, List[str]]):
        listings_provider_id (Union[Unset, str]):
        listings_channel_id (Union[Unset, str]):
        listings_path (Union[Unset, str]):
        listings_id (Union[Unset, str]):
        listings_channel_name (Union[Unset, str]):
        listings_channel_number (Union[Unset, str]):
        affiliate_call_sign (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    original_title: Union[Unset, str] = UNSET
    server_id: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    guid: Union[Unset, str] = UNSET
    etag: Union[Unset, str] = UNSET
    prefix: Union[Unset, str] = UNSET
    playlist_item_id: Union[Unset, str] = UNSET
    date_created: Union[Unset, None, datetime.datetime] = UNSET
    extra_type: Union[Unset, str] = UNSET
    sort_index_number: Union[Unset, None, int] = UNSET
    sort_parent_index_number: Union[Unset, None, int] = UNSET
    can_delete: Union[Unset, None, bool] = UNSET
    can_download: Union[Unset, None, bool] = UNSET
    supports_resume: Union[Unset, None, bool] = UNSET
    presentation_unique_key: Union[Unset, str] = UNSET
    preferred_metadata_language: Union[Unset, str] = UNSET
    preferred_metadata_country_code: Union[Unset, str] = UNSET
    supports_sync: Union[Unset, None, bool] = UNSET
    can_manage_access: Union[Unset, None, bool] = UNSET
    can_make_private: Union[Unset, None, bool] = UNSET
    can_make_public: Union[Unset, None, bool] = UNSET
    container: Union[Unset, str] = UNSET
    sort_name: Union[Unset, str] = UNSET
    forced_sort_name: Union[Unset, str] = UNSET
    video_3d_format: Union[Unset, Video3DFormat] = UNSET
    premiere_date: Union[Unset, None, datetime.datetime] = UNSET
    external_urls: Union[Unset, List["ExternalUrl"]] = UNSET
    media_sources: Union[Unset, List["MediaSourceInfo"]] = UNSET
    critic_rating: Union[Unset, None, float] = UNSET
    game_system_id: Union[Unset, None, int] = UNSET
    as_series: Union[Unset, None, bool] = UNSET
    game_system: Union[Unset, str] = UNSET
    production_locations: Union[Unset, List[str]] = UNSET
    path: Union[Unset, str] = UNSET
    official_rating: Union[Unset, str] = UNSET
    custom_rating: Union[Unset, str] = UNSET
    channel_id: Union[Unset, str] = UNSET
    channel_name: Union[Unset, str] = UNSET
    overview: Union[Unset, str] = UNSET
    taglines: Union[Unset, List[str]] = UNSET
    genres: Union[Unset, List[str]] = UNSET
    community_rating: Union[Unset, None, float] = UNSET
    run_time_ticks: Union[Unset, None, int] = UNSET
    size: Union[Unset, None, int] = UNSET
    file_name: Union[Unset, str] = UNSET
    bitrate: Union[Unset, None, int] = UNSET
    production_year: Union[Unset, None, int] = UNSET
    number: Union[Unset, str] = UNSET
    channel_number: Union[Unset, str] = UNSET
    index_number: Union[Unset, None, int] = UNSET
    index_number_end: Union[Unset, None, int] = UNSET
    parent_index_number: Union[Unset, None, int] = UNSET
    remote_trailers: Union[Unset, List["MediaUrl"]] = UNSET
    provider_ids: Union[Unset, "ProviderIdDictionary"] = UNSET
    is_folder: Union[Unset, None, bool] = UNSET
    parent_id: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    people: Union[Unset, List["BaseItemPerson"]] = UNSET
    studios: Union[Unset, List["NameLongIdPair"]] = UNSET
    genre_items: Union[Unset, List["NameLongIdPair"]] = UNSET
    tag_items: Union[Unset, List["NameLongIdPair"]] = UNSET
    parent_logo_item_id: Union[Unset, str] = UNSET
    parent_backdrop_item_id: Union[Unset, str] = UNSET
    parent_backdrop_image_tags: Union[Unset, List[str]] = UNSET
    local_trailer_count: Union[Unset, None, int] = UNSET
    user_data: Union[Unset, "UserItemDataDto"] = UNSET
    recursive_item_count: Union[Unset, None, int] = UNSET
    child_count: Union[Unset, None, int] = UNSET
    series_name: Union[Unset, str] = UNSET
    series_id: Union[Unset, str] = UNSET
    season_id: Union[Unset, str] = UNSET
    special_feature_count: Union[Unset, None, int] = UNSET
    display_preferences_id: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    air_days: Union[Unset, List[DayOfWeek]] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    primary_image_aspect_ratio: Union[Unset, None, float] = UNSET
    artists: Union[Unset, List[str]] = UNSET
    artist_items: Union[Unset, List["NameIdPair"]] = UNSET
    composers: Union[Unset, List["NameIdPair"]] = UNSET
    album: Union[Unset, str] = UNSET
    collection_type: Union[Unset, str] = UNSET
    display_order: Union[Unset, str] = UNSET
    album_id: Union[Unset, str] = UNSET
    album_primary_image_tag: Union[Unset, str] = UNSET
    series_primary_image_tag: Union[Unset, str] = UNSET
    album_artist: Union[Unset, str] = UNSET
    album_artists: Union[Unset, List["NameIdPair"]] = UNSET
    season_name: Union[Unset, str] = UNSET
    media_streams: Union[Unset, List["MediaStream"]] = UNSET
    part_count: Union[Unset, None, int] = UNSET
    image_tags: Union[Unset, "BaseItemDtoImageTags"] = UNSET
    backdrop_image_tags: Union[Unset, List[str]] = UNSET
    parent_logo_image_tag: Union[Unset, str] = UNSET
    series_studio: Union[Unset, str] = UNSET
    parent_thumb_item_id: Union[Unset, str] = UNSET
    parent_thumb_image_tag: Union[Unset, str] = UNSET
    chapters: Union[Unset, List["ChapterInfo"]] = UNSET
    location_type: Union[Unset, LocationType] = UNSET
    media_type: Union[Unset, str] = UNSET
    end_date: Union[Unset, None, datetime.datetime] = UNSET
    locked_fields: Union[Unset, List[MetadataFields]] = UNSET
    lock_data: Union[Unset, None, bool] = UNSET
    width: Union[Unset, None, int] = UNSET
    height: Union[Unset, None, int] = UNSET
    camera_make: Union[Unset, str] = UNSET
    camera_model: Union[Unset, str] = UNSET
    software: Union[Unset, str] = UNSET
    exposure_time: Union[Unset, None, float] = UNSET
    focal_length: Union[Unset, None, float] = UNSET
    image_orientation: Union[Unset, DrawingImageOrientation] = UNSET
    aperture: Union[Unset, None, float] = UNSET
    shutter_speed: Union[Unset, None, float] = UNSET
    latitude: Union[Unset, None, float] = UNSET
    longitude: Union[Unset, None, float] = UNSET
    altitude: Union[Unset, None, float] = UNSET
    iso_speed_rating: Union[Unset, None, int] = UNSET
    series_timer_id: Union[Unset, str] = UNSET
    channel_primary_image_tag: Union[Unset, str] = UNSET
    start_date: Union[Unset, None, datetime.datetime] = UNSET
    completion_percentage: Union[Unset, None, float] = UNSET
    is_repeat: Union[Unset, None, bool] = UNSET
    is_new: Union[Unset, None, bool] = UNSET
    episode_title: Union[Unset, str] = UNSET
    is_movie: Union[Unset, None, bool] = UNSET
    is_sports: Union[Unset, None, bool] = UNSET
    is_series: Union[Unset, None, bool] = UNSET
    is_live: Union[Unset, None, bool] = UNSET
    is_news: Union[Unset, None, bool] = UNSET
    is_kids: Union[Unset, None, bool] = UNSET
    is_premiere: Union[Unset, None, bool] = UNSET
    timer_type: Union[Unset, LiveTvTimerType] = UNSET
    disabled: Union[Unset, None, bool] = UNSET
    management_id: Union[Unset, str] = UNSET
    timer_id: Union[Unset, str] = UNSET
    current_program: Union[Unset, "BaseItemDto"] = UNSET
    movie_count: Union[Unset, None, int] = UNSET
    series_count: Union[Unset, None, int] = UNSET
    album_count: Union[Unset, None, int] = UNSET
    song_count: Union[Unset, None, int] = UNSET
    music_video_count: Union[Unset, None, int] = UNSET
    subviews: Union[Unset, List[str]] = UNSET
    listings_provider_id: Union[Unset, str] = UNSET
    listings_channel_id: Union[Unset, str] = UNSET
    listings_path: Union[Unset, str] = UNSET
    listings_id: Union[Unset, str] = UNSET
    listings_channel_name: Union[Unset, str] = UNSET
    listings_channel_number: Union[Unset, str] = UNSET
    affiliate_call_sign: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        original_title = self.original_title
        server_id = self.server_id
        id = self.id
        guid = self.guid
        etag = self.etag
        prefix = self.prefix
        playlist_item_id = self.playlist_item_id
        date_created: Union[Unset, None, str] = UNSET
        if not isinstance(self.date_created, Unset):
            date_created = self.date_created.isoformat() if self.date_created else None

        extra_type = self.extra_type
        sort_index_number = self.sort_index_number
        sort_parent_index_number = self.sort_parent_index_number
        can_delete = self.can_delete
        can_download = self.can_download
        supports_resume = self.supports_resume
        presentation_unique_key = self.presentation_unique_key
        preferred_metadata_language = self.preferred_metadata_language
        preferred_metadata_country_code = self.preferred_metadata_country_code
        supports_sync = self.supports_sync
        can_manage_access = self.can_manage_access
        can_make_private = self.can_make_private
        can_make_public = self.can_make_public
        container = self.container
        sort_name = self.sort_name
        forced_sort_name = self.forced_sort_name
        video_3d_format: Union[Unset, str] = UNSET
        if not isinstance(self.video_3d_format, Unset):
            video_3d_format = self.video_3d_format.value

        premiere_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.premiere_date, Unset):
            premiere_date = self.premiere_date.isoformat() if self.premiere_date else None

        external_urls: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.external_urls, Unset):
            external_urls = []
            for external_urls_item_data in self.external_urls:
                external_urls_item = external_urls_item_data.to_dict()

                external_urls.append(external_urls_item)

        media_sources: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.media_sources, Unset):
            media_sources = []
            for media_sources_item_data in self.media_sources:
                media_sources_item = media_sources_item_data.to_dict()

                media_sources.append(media_sources_item)

        critic_rating = self.critic_rating
        game_system_id = self.game_system_id
        as_series = self.as_series
        game_system = self.game_system
        production_locations: Union[Unset, List[str]] = UNSET
        if not isinstance(self.production_locations, Unset):
            production_locations = self.production_locations

        path = self.path
        official_rating = self.official_rating
        custom_rating = self.custom_rating
        channel_id = self.channel_id
        channel_name = self.channel_name
        overview = self.overview
        taglines: Union[Unset, List[str]] = UNSET
        if not isinstance(self.taglines, Unset):
            taglines = self.taglines

        genres: Union[Unset, List[str]] = UNSET
        if not isinstance(self.genres, Unset):
            genres = self.genres

        community_rating = self.community_rating
        run_time_ticks = self.run_time_ticks
        size = self.size
        file_name = self.file_name
        bitrate = self.bitrate
        production_year = self.production_year
        number = self.number
        channel_number = self.channel_number
        index_number = self.index_number
        index_number_end = self.index_number_end
        parent_index_number = self.parent_index_number
        remote_trailers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.remote_trailers, Unset):
            remote_trailers = []
            for remote_trailers_item_data in self.remote_trailers:
                remote_trailers_item = remote_trailers_item_data.to_dict()

                remote_trailers.append(remote_trailers_item)

        provider_ids: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.provider_ids, Unset):
            provider_ids = self.provider_ids.to_dict()

        is_folder = self.is_folder
        parent_id = self.parent_id
        type = self.type
        people: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.people, Unset):
            people = []
            for people_item_data in self.people:
                people_item = people_item_data.to_dict()

                people.append(people_item)

        studios: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.studios, Unset):
            studios = []
            for studios_item_data in self.studios:
                studios_item = studios_item_data.to_dict()

                studios.append(studios_item)

        genre_items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.genre_items, Unset):
            genre_items = []
            for genre_items_item_data in self.genre_items:
                genre_items_item = genre_items_item_data.to_dict()

                genre_items.append(genre_items_item)

        tag_items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tag_items, Unset):
            tag_items = []
            for tag_items_item_data in self.tag_items:
                tag_items_item = tag_items_item_data.to_dict()

                tag_items.append(tag_items_item)

        parent_logo_item_id = self.parent_logo_item_id
        parent_backdrop_item_id = self.parent_backdrop_item_id
        parent_backdrop_image_tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.parent_backdrop_image_tags, Unset):
            parent_backdrop_image_tags = self.parent_backdrop_image_tags

        local_trailer_count = self.local_trailer_count
        user_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user_data, Unset):
            user_data = self.user_data.to_dict()

        recursive_item_count = self.recursive_item_count
        child_count = self.child_count
        series_name = self.series_name
        series_id = self.series_id
        season_id = self.season_id
        special_feature_count = self.special_feature_count
        display_preferences_id = self.display_preferences_id
        status = self.status
        air_days: Union[Unset, List[str]] = UNSET
        if not isinstance(self.air_days, Unset):
            air_days = []
            for air_days_item_data in self.air_days:
                air_days_item = air_days_item_data.value

                air_days.append(air_days_item)

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        primary_image_aspect_ratio = self.primary_image_aspect_ratio
        artists: Union[Unset, List[str]] = UNSET
        if not isinstance(self.artists, Unset):
            artists = self.artists

        artist_items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.artist_items, Unset):
            artist_items = []
            for artist_items_item_data in self.artist_items:
                artist_items_item = artist_items_item_data.to_dict()

                artist_items.append(artist_items_item)

        composers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.composers, Unset):
            composers = []
            for composers_item_data in self.composers:
                composers_item = composers_item_data.to_dict()

                composers.append(composers_item)

        album = self.album
        collection_type = self.collection_type
        display_order = self.display_order
        album_id = self.album_id
        album_primary_image_tag = self.album_primary_image_tag
        series_primary_image_tag = self.series_primary_image_tag
        album_artist = self.album_artist
        album_artists: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.album_artists, Unset):
            album_artists = []
            for album_artists_item_data in self.album_artists:
                album_artists_item = album_artists_item_data.to_dict()

                album_artists.append(album_artists_item)

        season_name = self.season_name
        media_streams: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.media_streams, Unset):
            media_streams = []
            for media_streams_item_data in self.media_streams:
                media_streams_item = media_streams_item_data.to_dict()

                media_streams.append(media_streams_item)

        part_count = self.part_count
        image_tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.image_tags, Unset):
            image_tags = self.image_tags.to_dict()

        backdrop_image_tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.backdrop_image_tags, Unset):
            backdrop_image_tags = self.backdrop_image_tags

        parent_logo_image_tag = self.parent_logo_image_tag
        series_studio = self.series_studio
        parent_thumb_item_id = self.parent_thumb_item_id
        parent_thumb_image_tag = self.parent_thumb_image_tag
        chapters: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.chapters, Unset):
            chapters = []
            for chapters_item_data in self.chapters:
                chapters_item = chapters_item_data.to_dict()

                chapters.append(chapters_item)

        location_type: Union[Unset, str] = UNSET
        if not isinstance(self.location_type, Unset):
            location_type = self.location_type.value

        media_type = self.media_type
        end_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat() if self.end_date else None

        locked_fields: Union[Unset, List[str]] = UNSET
        if not isinstance(self.locked_fields, Unset):
            locked_fields = []
            for locked_fields_item_data in self.locked_fields:
                locked_fields_item = locked_fields_item_data.value

                locked_fields.append(locked_fields_item)

        lock_data = self.lock_data
        width = self.width
        height = self.height
        camera_make = self.camera_make
        camera_model = self.camera_model
        software = self.software
        exposure_time = self.exposure_time
        focal_length = self.focal_length
        image_orientation: Union[Unset, str] = UNSET
        if not isinstance(self.image_orientation, Unset):
            image_orientation = self.image_orientation.value

        aperture = self.aperture
        shutter_speed = self.shutter_speed
        latitude = self.latitude
        longitude = self.longitude
        altitude = self.altitude
        iso_speed_rating = self.iso_speed_rating
        series_timer_id = self.series_timer_id
        channel_primary_image_tag = self.channel_primary_image_tag
        start_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat() if self.start_date else None

        completion_percentage = self.completion_percentage
        is_repeat = self.is_repeat
        is_new = self.is_new
        episode_title = self.episode_title
        is_movie = self.is_movie
        is_sports = self.is_sports
        is_series = self.is_series
        is_live = self.is_live
        is_news = self.is_news
        is_kids = self.is_kids
        is_premiere = self.is_premiere
        timer_type: Union[Unset, str] = UNSET
        if not isinstance(self.timer_type, Unset):
            timer_type = self.timer_type.value

        disabled = self.disabled
        management_id = self.management_id
        timer_id = self.timer_id
        current_program: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.current_program, Unset):
            current_program = self.current_program.to_dict()

        movie_count = self.movie_count
        series_count = self.series_count
        album_count = self.album_count
        song_count = self.song_count
        music_video_count = self.music_video_count
        subviews: Union[Unset, List[str]] = UNSET
        if not isinstance(self.subviews, Unset):
            subviews = self.subviews

        listings_provider_id = self.listings_provider_id
        listings_channel_id = self.listings_channel_id
        listings_path = self.listings_path
        listings_id = self.listings_id
        listings_channel_name = self.listings_channel_name
        listings_channel_number = self.listings_channel_number
        affiliate_call_sign = self.affiliate_call_sign

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if original_title is not UNSET:
            field_dict["OriginalTitle"] = original_title
        if server_id is not UNSET:
            field_dict["ServerId"] = server_id
        if id is not UNSET:
            field_dict["Id"] = id
        if guid is not UNSET:
            field_dict["Guid"] = guid
        if etag is not UNSET:
            field_dict["Etag"] = etag
        if prefix is not UNSET:
            field_dict["Prefix"] = prefix
        if playlist_item_id is not UNSET:
            field_dict["PlaylistItemId"] = playlist_item_id
        if date_created is not UNSET:
            field_dict["DateCreated"] = date_created
        if extra_type is not UNSET:
            field_dict["ExtraType"] = extra_type
        if sort_index_number is not UNSET:
            field_dict["SortIndexNumber"] = sort_index_number
        if sort_parent_index_number is not UNSET:
            field_dict["SortParentIndexNumber"] = sort_parent_index_number
        if can_delete is not UNSET:
            field_dict["CanDelete"] = can_delete
        if can_download is not UNSET:
            field_dict["CanDownload"] = can_download
        if supports_resume is not UNSET:
            field_dict["SupportsResume"] = supports_resume
        if presentation_unique_key is not UNSET:
            field_dict["PresentationUniqueKey"] = presentation_unique_key
        if preferred_metadata_language is not UNSET:
            field_dict["PreferredMetadataLanguage"] = preferred_metadata_language
        if preferred_metadata_country_code is not UNSET:
            field_dict["PreferredMetadataCountryCode"] = preferred_metadata_country_code
        if supports_sync is not UNSET:
            field_dict["SupportsSync"] = supports_sync
        if can_manage_access is not UNSET:
            field_dict["CanManageAccess"] = can_manage_access
        if can_make_private is not UNSET:
            field_dict["CanMakePrivate"] = can_make_private
        if can_make_public is not UNSET:
            field_dict["CanMakePublic"] = can_make_public
        if container is not UNSET:
            field_dict["Container"] = container
        if sort_name is not UNSET:
            field_dict["SortName"] = sort_name
        if forced_sort_name is not UNSET:
            field_dict["ForcedSortName"] = forced_sort_name
        if video_3d_format is not UNSET:
            field_dict["Video3DFormat"] = video_3d_format
        if premiere_date is not UNSET:
            field_dict["PremiereDate"] = premiere_date
        if external_urls is not UNSET:
            field_dict["ExternalUrls"] = external_urls
        if media_sources is not UNSET:
            field_dict["MediaSources"] = media_sources
        if critic_rating is not UNSET:
            field_dict["CriticRating"] = critic_rating
        if game_system_id is not UNSET:
            field_dict["GameSystemId"] = game_system_id
        if as_series is not UNSET:
            field_dict["AsSeries"] = as_series
        if game_system is not UNSET:
            field_dict["GameSystem"] = game_system
        if production_locations is not UNSET:
            field_dict["ProductionLocations"] = production_locations
        if path is not UNSET:
            field_dict["Path"] = path
        if official_rating is not UNSET:
            field_dict["OfficialRating"] = official_rating
        if custom_rating is not UNSET:
            field_dict["CustomRating"] = custom_rating
        if channel_id is not UNSET:
            field_dict["ChannelId"] = channel_id
        if channel_name is not UNSET:
            field_dict["ChannelName"] = channel_name
        if overview is not UNSET:
            field_dict["Overview"] = overview
        if taglines is not UNSET:
            field_dict["Taglines"] = taglines
        if genres is not UNSET:
            field_dict["Genres"] = genres
        if community_rating is not UNSET:
            field_dict["CommunityRating"] = community_rating
        if run_time_ticks is not UNSET:
            field_dict["RunTimeTicks"] = run_time_ticks
        if size is not UNSET:
            field_dict["Size"] = size
        if file_name is not UNSET:
            field_dict["FileName"] = file_name
        if bitrate is not UNSET:
            field_dict["Bitrate"] = bitrate
        if production_year is not UNSET:
            field_dict["ProductionYear"] = production_year
        if number is not UNSET:
            field_dict["Number"] = number
        if channel_number is not UNSET:
            field_dict["ChannelNumber"] = channel_number
        if index_number is not UNSET:
            field_dict["IndexNumber"] = index_number
        if index_number_end is not UNSET:
            field_dict["IndexNumberEnd"] = index_number_end
        if parent_index_number is not UNSET:
            field_dict["ParentIndexNumber"] = parent_index_number
        if remote_trailers is not UNSET:
            field_dict["RemoteTrailers"] = remote_trailers
        if provider_ids is not UNSET:
            field_dict["ProviderIds"] = provider_ids
        if is_folder is not UNSET:
            field_dict["IsFolder"] = is_folder
        if parent_id is not UNSET:
            field_dict["ParentId"] = parent_id
        if type is not UNSET:
            field_dict["Type"] = type
        if people is not UNSET:
            field_dict["People"] = people
        if studios is not UNSET:
            field_dict["Studios"] = studios
        if genre_items is not UNSET:
            field_dict["GenreItems"] = genre_items
        if tag_items is not UNSET:
            field_dict["TagItems"] = tag_items
        if parent_logo_item_id is not UNSET:
            field_dict["ParentLogoItemId"] = parent_logo_item_id
        if parent_backdrop_item_id is not UNSET:
            field_dict["ParentBackdropItemId"] = parent_backdrop_item_id
        if parent_backdrop_image_tags is not UNSET:
            field_dict["ParentBackdropImageTags"] = parent_backdrop_image_tags
        if local_trailer_count is not UNSET:
            field_dict["LocalTrailerCount"] = local_trailer_count
        if user_data is not UNSET:
            field_dict["UserData"] = user_data
        if recursive_item_count is not UNSET:
            field_dict["RecursiveItemCount"] = recursive_item_count
        if child_count is not UNSET:
            field_dict["ChildCount"] = child_count
        if series_name is not UNSET:
            field_dict["SeriesName"] = series_name
        if series_id is not UNSET:
            field_dict["SeriesId"] = series_id
        if season_id is not UNSET:
            field_dict["SeasonId"] = season_id
        if special_feature_count is not UNSET:
            field_dict["SpecialFeatureCount"] = special_feature_count
        if display_preferences_id is not UNSET:
            field_dict["DisplayPreferencesId"] = display_preferences_id
        if status is not UNSET:
            field_dict["Status"] = status
        if air_days is not UNSET:
            field_dict["AirDays"] = air_days
        if tags is not UNSET:
            field_dict["Tags"] = tags
        if primary_image_aspect_ratio is not UNSET:
            field_dict["PrimaryImageAspectRatio"] = primary_image_aspect_ratio
        if artists is not UNSET:
            field_dict["Artists"] = artists
        if artist_items is not UNSET:
            field_dict["ArtistItems"] = artist_items
        if composers is not UNSET:
            field_dict["Composers"] = composers
        if album is not UNSET:
            field_dict["Album"] = album
        if collection_type is not UNSET:
            field_dict["CollectionType"] = collection_type
        if display_order is not UNSET:
            field_dict["DisplayOrder"] = display_order
        if album_id is not UNSET:
            field_dict["AlbumId"] = album_id
        if album_primary_image_tag is not UNSET:
            field_dict["AlbumPrimaryImageTag"] = album_primary_image_tag
        if series_primary_image_tag is not UNSET:
            field_dict["SeriesPrimaryImageTag"] = series_primary_image_tag
        if album_artist is not UNSET:
            field_dict["AlbumArtist"] = album_artist
        if album_artists is not UNSET:
            field_dict["AlbumArtists"] = album_artists
        if season_name is not UNSET:
            field_dict["SeasonName"] = season_name
        if media_streams is not UNSET:
            field_dict["MediaStreams"] = media_streams
        if part_count is not UNSET:
            field_dict["PartCount"] = part_count
        if image_tags is not UNSET:
            field_dict["ImageTags"] = image_tags
        if backdrop_image_tags is not UNSET:
            field_dict["BackdropImageTags"] = backdrop_image_tags
        if parent_logo_image_tag is not UNSET:
            field_dict["ParentLogoImageTag"] = parent_logo_image_tag
        if series_studio is not UNSET:
            field_dict["SeriesStudio"] = series_studio
        if parent_thumb_item_id is not UNSET:
            field_dict["ParentThumbItemId"] = parent_thumb_item_id
        if parent_thumb_image_tag is not UNSET:
            field_dict["ParentThumbImageTag"] = parent_thumb_image_tag
        if chapters is not UNSET:
            field_dict["Chapters"] = chapters
        if location_type is not UNSET:
            field_dict["LocationType"] = location_type
        if media_type is not UNSET:
            field_dict["MediaType"] = media_type
        if end_date is not UNSET:
            field_dict["EndDate"] = end_date
        if locked_fields is not UNSET:
            field_dict["LockedFields"] = locked_fields
        if lock_data is not UNSET:
            field_dict["LockData"] = lock_data
        if width is not UNSET:
            field_dict["Width"] = width
        if height is not UNSET:
            field_dict["Height"] = height
        if camera_make is not UNSET:
            field_dict["CameraMake"] = camera_make
        if camera_model is not UNSET:
            field_dict["CameraModel"] = camera_model
        if software is not UNSET:
            field_dict["Software"] = software
        if exposure_time is not UNSET:
            field_dict["ExposureTime"] = exposure_time
        if focal_length is not UNSET:
            field_dict["FocalLength"] = focal_length
        if image_orientation is not UNSET:
            field_dict["ImageOrientation"] = image_orientation
        if aperture is not UNSET:
            field_dict["Aperture"] = aperture
        if shutter_speed is not UNSET:
            field_dict["ShutterSpeed"] = shutter_speed
        if latitude is not UNSET:
            field_dict["Latitude"] = latitude
        if longitude is not UNSET:
            field_dict["Longitude"] = longitude
        if altitude is not UNSET:
            field_dict["Altitude"] = altitude
        if iso_speed_rating is not UNSET:
            field_dict["IsoSpeedRating"] = iso_speed_rating
        if series_timer_id is not UNSET:
            field_dict["SeriesTimerId"] = series_timer_id
        if channel_primary_image_tag is not UNSET:
            field_dict["ChannelPrimaryImageTag"] = channel_primary_image_tag
        if start_date is not UNSET:
            field_dict["StartDate"] = start_date
        if completion_percentage is not UNSET:
            field_dict["CompletionPercentage"] = completion_percentage
        if is_repeat is not UNSET:
            field_dict["IsRepeat"] = is_repeat
        if is_new is not UNSET:
            field_dict["IsNew"] = is_new
        if episode_title is not UNSET:
            field_dict["EpisodeTitle"] = episode_title
        if is_movie is not UNSET:
            field_dict["IsMovie"] = is_movie
        if is_sports is not UNSET:
            field_dict["IsSports"] = is_sports
        if is_series is not UNSET:
            field_dict["IsSeries"] = is_series
        if is_live is not UNSET:
            field_dict["IsLive"] = is_live
        if is_news is not UNSET:
            field_dict["IsNews"] = is_news
        if is_kids is not UNSET:
            field_dict["IsKids"] = is_kids
        if is_premiere is not UNSET:
            field_dict["IsPremiere"] = is_premiere
        if timer_type is not UNSET:
            field_dict["TimerType"] = timer_type
        if disabled is not UNSET:
            field_dict["Disabled"] = disabled
        if management_id is not UNSET:
            field_dict["ManagementId"] = management_id
        if timer_id is not UNSET:
            field_dict["TimerId"] = timer_id
        if current_program is not UNSET:
            field_dict["CurrentProgram"] = current_program
        if movie_count is not UNSET:
            field_dict["MovieCount"] = movie_count
        if series_count is not UNSET:
            field_dict["SeriesCount"] = series_count
        if album_count is not UNSET:
            field_dict["AlbumCount"] = album_count
        if song_count is not UNSET:
            field_dict["SongCount"] = song_count
        if music_video_count is not UNSET:
            field_dict["MusicVideoCount"] = music_video_count
        if subviews is not UNSET:
            field_dict["Subviews"] = subviews
        if listings_provider_id is not UNSET:
            field_dict["ListingsProviderId"] = listings_provider_id
        if listings_channel_id is not UNSET:
            field_dict["ListingsChannelId"] = listings_channel_id
        if listings_path is not UNSET:
            field_dict["ListingsPath"] = listings_path
        if listings_id is not UNSET:
            field_dict["ListingsId"] = listings_id
        if listings_channel_name is not UNSET:
            field_dict["ListingsChannelName"] = listings_channel_name
        if listings_channel_number is not UNSET:
            field_dict["ListingsChannelNumber"] = listings_channel_number
        if affiliate_call_sign is not UNSET:
            field_dict["AffiliateCallSign"] = affiliate_call_sign

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.base_item_dto_image_tags import BaseItemDtoImageTags
        from ..models.base_item_person import BaseItemPerson
        from ..models.chapter_info import ChapterInfo
        from ..models.external_url import ExternalUrl
        from ..models.media_source_info import MediaSourceInfo
        from ..models.media_stream import MediaStream
        from ..models.media_url import MediaUrl
        from ..models.name_id_pair import NameIdPair
        from ..models.name_long_id_pair import NameLongIdPair
        from ..models.provider_id_dictionary import ProviderIdDictionary
        from ..models.user_item_data_dto import UserItemDataDto

        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        original_title = d.pop("OriginalTitle", UNSET)

        server_id = d.pop("ServerId", UNSET)

        id = d.pop("Id", UNSET)

        guid = d.pop("Guid", UNSET)

        etag = d.pop("Etag", UNSET)

        prefix = d.pop("Prefix", UNSET)

        playlist_item_id = d.pop("PlaylistItemId", UNSET)

        _date_created = d.pop("DateCreated", UNSET)
        date_created: Union[Unset, None, datetime.datetime]
        if _date_created is None:
            date_created = None
        elif isinstance(_date_created, Unset):
            date_created = UNSET
        else:
            date_created = isoparse(_date_created)

        extra_type = d.pop("ExtraType", UNSET)

        sort_index_number = d.pop("SortIndexNumber", UNSET)

        sort_parent_index_number = d.pop("SortParentIndexNumber", UNSET)

        can_delete = d.pop("CanDelete", UNSET)

        can_download = d.pop("CanDownload", UNSET)

        supports_resume = d.pop("SupportsResume", UNSET)

        presentation_unique_key = d.pop("PresentationUniqueKey", UNSET)

        preferred_metadata_language = d.pop("PreferredMetadataLanguage", UNSET)

        preferred_metadata_country_code = d.pop("PreferredMetadataCountryCode", UNSET)

        supports_sync = d.pop("SupportsSync", UNSET)

        can_manage_access = d.pop("CanManageAccess", UNSET)

        can_make_private = d.pop("CanMakePrivate", UNSET)

        can_make_public = d.pop("CanMakePublic", UNSET)

        container = d.pop("Container", UNSET)

        sort_name = d.pop("SortName", UNSET)

        forced_sort_name = d.pop("ForcedSortName", UNSET)

        _video_3d_format = d.pop("Video3DFormat", UNSET)
        video_3d_format: Union[Unset, Video3DFormat]
        if isinstance(_video_3d_format, Unset):
            video_3d_format = UNSET
        else:
            video_3d_format = Video3DFormat(_video_3d_format)

        _premiere_date = d.pop("PremiereDate", UNSET)
        premiere_date: Union[Unset, None, datetime.datetime]
        if _premiere_date is None:
            premiere_date = None
        elif isinstance(_premiere_date, Unset):
            premiere_date = UNSET
        else:
            premiere_date = isoparse(_premiere_date)

        external_urls = []
        _external_urls = d.pop("ExternalUrls", UNSET)
        for external_urls_item_data in _external_urls or []:
            external_urls_item = ExternalUrl.from_dict(external_urls_item_data)

            external_urls.append(external_urls_item)

        media_sources = []
        _media_sources = d.pop("MediaSources", UNSET)
        for media_sources_item_data in _media_sources or []:
            media_sources_item = MediaSourceInfo.from_dict(media_sources_item_data)

            media_sources.append(media_sources_item)

        critic_rating = d.pop("CriticRating", UNSET)

        game_system_id = d.pop("GameSystemId", UNSET)

        as_series = d.pop("AsSeries", UNSET)

        game_system = d.pop("GameSystem", UNSET)

        production_locations = cast(List[str], d.pop("ProductionLocations", UNSET))

        path = d.pop("Path", UNSET)

        official_rating = d.pop("OfficialRating", UNSET)

        custom_rating = d.pop("CustomRating", UNSET)

        channel_id = d.pop("ChannelId", UNSET)

        channel_name = d.pop("ChannelName", UNSET)

        overview = d.pop("Overview", UNSET)

        taglines = cast(List[str], d.pop("Taglines", UNSET))

        genres = cast(List[str], d.pop("Genres", UNSET))

        community_rating = d.pop("CommunityRating", UNSET)

        run_time_ticks = d.pop("RunTimeTicks", UNSET)

        size = d.pop("Size", UNSET)

        file_name = d.pop("FileName", UNSET)

        bitrate = d.pop("Bitrate", UNSET)

        production_year = d.pop("ProductionYear", UNSET)

        number = d.pop("Number", UNSET)

        channel_number = d.pop("ChannelNumber", UNSET)

        index_number = d.pop("IndexNumber", UNSET)

        index_number_end = d.pop("IndexNumberEnd", UNSET)

        parent_index_number = d.pop("ParentIndexNumber", UNSET)

        remote_trailers = []
        _remote_trailers = d.pop("RemoteTrailers", UNSET)
        for remote_trailers_item_data in _remote_trailers or []:
            remote_trailers_item = MediaUrl.from_dict(remote_trailers_item_data)

            remote_trailers.append(remote_trailers_item)

        _provider_ids = d.pop("ProviderIds", UNSET)
        provider_ids: Union[Unset, ProviderIdDictionary]
        if isinstance(_provider_ids, Unset):
            provider_ids = UNSET
        else:
            provider_ids = ProviderIdDictionary.from_dict(_provider_ids)

        is_folder = d.pop("IsFolder", UNSET)

        parent_id = d.pop("ParentId", UNSET)

        type = d.pop("Type", UNSET)

        people = []
        _people = d.pop("People", UNSET)
        for people_item_data in _people or []:
            people_item = BaseItemPerson.from_dict(people_item_data)

            people.append(people_item)

        studios = []
        _studios = d.pop("Studios", UNSET)
        for studios_item_data in _studios or []:
            studios_item = NameLongIdPair.from_dict(studios_item_data)

            studios.append(studios_item)

        genre_items = []
        _genre_items = d.pop("GenreItems", UNSET)
        for genre_items_item_data in _genre_items or []:
            genre_items_item = NameLongIdPair.from_dict(genre_items_item_data)

            genre_items.append(genre_items_item)

        tag_items = []
        _tag_items = d.pop("TagItems", UNSET)
        for tag_items_item_data in _tag_items or []:
            tag_items_item = NameLongIdPair.from_dict(tag_items_item_data)

            tag_items.append(tag_items_item)

        parent_logo_item_id = d.pop("ParentLogoItemId", UNSET)

        parent_backdrop_item_id = d.pop("ParentBackdropItemId", UNSET)

        parent_backdrop_image_tags = cast(List[str], d.pop("ParentBackdropImageTags", UNSET))

        local_trailer_count = d.pop("LocalTrailerCount", UNSET)

        _user_data = d.pop("UserData", UNSET)
        user_data: Union[Unset, UserItemDataDto]
        if isinstance(_user_data, Unset):
            user_data = UNSET
        else:
            user_data = UserItemDataDto.from_dict(_user_data)

        recursive_item_count = d.pop("RecursiveItemCount", UNSET)

        child_count = d.pop("ChildCount", UNSET)

        series_name = d.pop("SeriesName", UNSET)

        series_id = d.pop("SeriesId", UNSET)

        season_id = d.pop("SeasonId", UNSET)

        special_feature_count = d.pop("SpecialFeatureCount", UNSET)

        display_preferences_id = d.pop("DisplayPreferencesId", UNSET)

        status = d.pop("Status", UNSET)

        air_days = []
        _air_days = d.pop("AirDays", UNSET)
        for air_days_item_data in _air_days or []:
            air_days_item = DayOfWeek(air_days_item_data)

            air_days.append(air_days_item)

        tags = cast(List[str], d.pop("Tags", UNSET))

        primary_image_aspect_ratio = d.pop("PrimaryImageAspectRatio", UNSET)

        artists = cast(List[str], d.pop("Artists", UNSET))

        artist_items = []
        _artist_items = d.pop("ArtistItems", UNSET)
        for artist_items_item_data in _artist_items or []:
            artist_items_item = NameIdPair.from_dict(artist_items_item_data)

            artist_items.append(artist_items_item)

        composers = []
        _composers = d.pop("Composers", UNSET)
        for composers_item_data in _composers or []:
            composers_item = NameIdPair.from_dict(composers_item_data)

            composers.append(composers_item)

        album = d.pop("Album", UNSET)

        collection_type = d.pop("CollectionType", UNSET)

        display_order = d.pop("DisplayOrder", UNSET)

        album_id = d.pop("AlbumId", UNSET)

        album_primary_image_tag = d.pop("AlbumPrimaryImageTag", UNSET)

        series_primary_image_tag = d.pop("SeriesPrimaryImageTag", UNSET)

        album_artist = d.pop("AlbumArtist", UNSET)

        album_artists = []
        _album_artists = d.pop("AlbumArtists", UNSET)
        for album_artists_item_data in _album_artists or []:
            album_artists_item = NameIdPair.from_dict(album_artists_item_data)

            album_artists.append(album_artists_item)

        season_name = d.pop("SeasonName", UNSET)

        media_streams = []
        _media_streams = d.pop("MediaStreams", UNSET)
        for media_streams_item_data in _media_streams or []:
            media_streams_item = MediaStream.from_dict(media_streams_item_data)

            media_streams.append(media_streams_item)

        part_count = d.pop("PartCount", UNSET)

        _image_tags = d.pop("ImageTags", UNSET)
        image_tags: Union[Unset, BaseItemDtoImageTags]
        if isinstance(_image_tags, Unset):
            image_tags = UNSET
        else:
            image_tags = BaseItemDtoImageTags.from_dict(_image_tags)

        backdrop_image_tags = cast(List[str], d.pop("BackdropImageTags", UNSET))

        parent_logo_image_tag = d.pop("ParentLogoImageTag", UNSET)

        series_studio = d.pop("SeriesStudio", UNSET)

        parent_thumb_item_id = d.pop("ParentThumbItemId", UNSET)

        parent_thumb_image_tag = d.pop("ParentThumbImageTag", UNSET)

        chapters = []
        _chapters = d.pop("Chapters", UNSET)
        for chapters_item_data in _chapters or []:
            chapters_item = ChapterInfo.from_dict(chapters_item_data)

            chapters.append(chapters_item)

        _location_type = d.pop("LocationType", UNSET)
        location_type: Union[Unset, LocationType]
        if isinstance(_location_type, Unset):
            location_type = UNSET
        else:
            location_type = LocationType(_location_type)

        media_type = d.pop("MediaType", UNSET)

        _end_date = d.pop("EndDate", UNSET)
        end_date: Union[Unset, None, datetime.datetime]
        if _end_date is None:
            end_date = None
        elif isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date)

        locked_fields = []
        _locked_fields = d.pop("LockedFields", UNSET)
        for locked_fields_item_data in _locked_fields or []:
            locked_fields_item = MetadataFields(locked_fields_item_data)

            locked_fields.append(locked_fields_item)

        lock_data = d.pop("LockData", UNSET)

        width = d.pop("Width", UNSET)

        height = d.pop("Height", UNSET)

        camera_make = d.pop("CameraMake", UNSET)

        camera_model = d.pop("CameraModel", UNSET)

        software = d.pop("Software", UNSET)

        exposure_time = d.pop("ExposureTime", UNSET)

        focal_length = d.pop("FocalLength", UNSET)

        _image_orientation = d.pop("ImageOrientation", UNSET)
        image_orientation: Union[Unset, DrawingImageOrientation]
        if isinstance(_image_orientation, Unset):
            image_orientation = UNSET
        else:
            image_orientation = DrawingImageOrientation(_image_orientation)

        aperture = d.pop("Aperture", UNSET)

        shutter_speed = d.pop("ShutterSpeed", UNSET)

        latitude = d.pop("Latitude", UNSET)

        longitude = d.pop("Longitude", UNSET)

        altitude = d.pop("Altitude", UNSET)

        iso_speed_rating = d.pop("IsoSpeedRating", UNSET)

        series_timer_id = d.pop("SeriesTimerId", UNSET)

        channel_primary_image_tag = d.pop("ChannelPrimaryImageTag", UNSET)

        _start_date = d.pop("StartDate", UNSET)
        start_date: Union[Unset, None, datetime.datetime]
        if _start_date is None:
            start_date = None
        elif isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date)

        completion_percentage = d.pop("CompletionPercentage", UNSET)

        is_repeat = d.pop("IsRepeat", UNSET)

        is_new = d.pop("IsNew", UNSET)

        episode_title = d.pop("EpisodeTitle", UNSET)

        is_movie = d.pop("IsMovie", UNSET)

        is_sports = d.pop("IsSports", UNSET)

        is_series = d.pop("IsSeries", UNSET)

        is_live = d.pop("IsLive", UNSET)

        is_news = d.pop("IsNews", UNSET)

        is_kids = d.pop("IsKids", UNSET)

        is_premiere = d.pop("IsPremiere", UNSET)

        _timer_type = d.pop("TimerType", UNSET)
        timer_type: Union[Unset, LiveTvTimerType]
        if isinstance(_timer_type, Unset):
            timer_type = UNSET
        else:
            timer_type = LiveTvTimerType(_timer_type)

        disabled = d.pop("Disabled", UNSET)

        management_id = d.pop("ManagementId", UNSET)

        timer_id = d.pop("TimerId", UNSET)

        _current_program = d.pop("CurrentProgram", UNSET)
        current_program: Union[Unset, BaseItemDto]
        if isinstance(_current_program, Unset):
            current_program = UNSET
        else:
            current_program = BaseItemDto.from_dict(_current_program)

        movie_count = d.pop("MovieCount", UNSET)

        series_count = d.pop("SeriesCount", UNSET)

        album_count = d.pop("AlbumCount", UNSET)

        song_count = d.pop("SongCount", UNSET)

        music_video_count = d.pop("MusicVideoCount", UNSET)

        subviews = cast(List[str], d.pop("Subviews", UNSET))

        listings_provider_id = d.pop("ListingsProviderId", UNSET)

        listings_channel_id = d.pop("ListingsChannelId", UNSET)

        listings_path = d.pop("ListingsPath", UNSET)

        listings_id = d.pop("ListingsId", UNSET)

        listings_channel_name = d.pop("ListingsChannelName", UNSET)

        listings_channel_number = d.pop("ListingsChannelNumber", UNSET)

        affiliate_call_sign = d.pop("AffiliateCallSign", UNSET)

        base_item_dto = cls(
            name=name,
            original_title=original_title,
            server_id=server_id,
            id=id,
            guid=guid,
            etag=etag,
            prefix=prefix,
            playlist_item_id=playlist_item_id,
            date_created=date_created,
            extra_type=extra_type,
            sort_index_number=sort_index_number,
            sort_parent_index_number=sort_parent_index_number,
            can_delete=can_delete,
            can_download=can_download,
            supports_resume=supports_resume,
            presentation_unique_key=presentation_unique_key,
            preferred_metadata_language=preferred_metadata_language,
            preferred_metadata_country_code=preferred_metadata_country_code,
            supports_sync=supports_sync,
            can_manage_access=can_manage_access,
            can_make_private=can_make_private,
            can_make_public=can_make_public,
            container=container,
            sort_name=sort_name,
            forced_sort_name=forced_sort_name,
            video_3d_format=video_3d_format,
            premiere_date=premiere_date,
            external_urls=external_urls,
            media_sources=media_sources,
            critic_rating=critic_rating,
            game_system_id=game_system_id,
            as_series=as_series,
            game_system=game_system,
            production_locations=production_locations,
            path=path,
            official_rating=official_rating,
            custom_rating=custom_rating,
            channel_id=channel_id,
            channel_name=channel_name,
            overview=overview,
            taglines=taglines,
            genres=genres,
            community_rating=community_rating,
            run_time_ticks=run_time_ticks,
            size=size,
            file_name=file_name,
            bitrate=bitrate,
            production_year=production_year,
            number=number,
            channel_number=channel_number,
            index_number=index_number,
            index_number_end=index_number_end,
            parent_index_number=parent_index_number,
            remote_trailers=remote_trailers,
            provider_ids=provider_ids,
            is_folder=is_folder,
            parent_id=parent_id,
            type=type,
            people=people,
            studios=studios,
            genre_items=genre_items,
            tag_items=tag_items,
            parent_logo_item_id=parent_logo_item_id,
            parent_backdrop_item_id=parent_backdrop_item_id,
            parent_backdrop_image_tags=parent_backdrop_image_tags,
            local_trailer_count=local_trailer_count,
            user_data=user_data,
            recursive_item_count=recursive_item_count,
            child_count=child_count,
            series_name=series_name,
            series_id=series_id,
            season_id=season_id,
            special_feature_count=special_feature_count,
            display_preferences_id=display_preferences_id,
            status=status,
            air_days=air_days,
            tags=tags,
            primary_image_aspect_ratio=primary_image_aspect_ratio,
            artists=artists,
            artist_items=artist_items,
            composers=composers,
            album=album,
            collection_type=collection_type,
            display_order=display_order,
            album_id=album_id,
            album_primary_image_tag=album_primary_image_tag,
            series_primary_image_tag=series_primary_image_tag,
            album_artist=album_artist,
            album_artists=album_artists,
            season_name=season_name,
            media_streams=media_streams,
            part_count=part_count,
            image_tags=image_tags,
            backdrop_image_tags=backdrop_image_tags,
            parent_logo_image_tag=parent_logo_image_tag,
            series_studio=series_studio,
            parent_thumb_item_id=parent_thumb_item_id,
            parent_thumb_image_tag=parent_thumb_image_tag,
            chapters=chapters,
            location_type=location_type,
            media_type=media_type,
            end_date=end_date,
            locked_fields=locked_fields,
            lock_data=lock_data,
            width=width,
            height=height,
            camera_make=camera_make,
            camera_model=camera_model,
            software=software,
            exposure_time=exposure_time,
            focal_length=focal_length,
            image_orientation=image_orientation,
            aperture=aperture,
            shutter_speed=shutter_speed,
            latitude=latitude,
            longitude=longitude,
            altitude=altitude,
            iso_speed_rating=iso_speed_rating,
            series_timer_id=series_timer_id,
            channel_primary_image_tag=channel_primary_image_tag,
            start_date=start_date,
            completion_percentage=completion_percentage,
            is_repeat=is_repeat,
            is_new=is_new,
            episode_title=episode_title,
            is_movie=is_movie,
            is_sports=is_sports,
            is_series=is_series,
            is_live=is_live,
            is_news=is_news,
            is_kids=is_kids,
            is_premiere=is_premiere,
            timer_type=timer_type,
            disabled=disabled,
            management_id=management_id,
            timer_id=timer_id,
            current_program=current_program,
            movie_count=movie_count,
            series_count=series_count,
            album_count=album_count,
            song_count=song_count,
            music_video_count=music_video_count,
            subviews=subviews,
            listings_provider_id=listings_provider_id,
            listings_channel_id=listings_channel_id,
            listings_path=listings_path,
            listings_id=listings_id,
            listings_channel_name=listings_channel_name,
            listings_channel_number=listings_channel_number,
            affiliate_call_sign=affiliate_call_sign,
        )

        base_item_dto.additional_properties = d
        return base_item_dto

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
