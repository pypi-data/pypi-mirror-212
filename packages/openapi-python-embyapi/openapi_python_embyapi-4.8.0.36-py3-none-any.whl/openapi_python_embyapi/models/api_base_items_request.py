from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.day_of_week import DayOfWeek
from ..models.library_item_link_type import LibraryItemLinkType
from ..models.live_tv_keyword_type import LiveTvKeywordType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiBaseItemsRequest")


@attr.s(auto_attribs=True)
class ApiBaseItemsRequest:
    """
    Attributes:
        is_4k (Union[Unset, None, bool]):
        enable_total_record_count (Union[Unset, bool]):
        recording_keyword (Union[Unset, str]):
        recording_keyword_type (Union[Unset, LiveTvKeywordType]):
        random_seed (Union[Unset, int]):
        genre_ids (Union[Unset, str]):
        collection_ids (Union[Unset, str]):
        tag_ids (Union[Unset, str]):
        exclude_artist_ids (Union[Unset, str]):
        album_artist_ids (Union[Unset, str]):
        contributing_artist_ids (Union[Unset, str]):
        album_ids (Union[Unset, str]):
        outer_ids (Union[Unset, str]):
        list_item_ids (Union[Unset, str]):
        audio_languages (Union[Unset, str]):
        subtitle_languages (Union[Unset, str]):
        group_items_into (Union[Unset, LibraryItemLinkType]):
        min_width (Union[Unset, None, int]):
        min_height (Union[Unset, None, int]):
        max_width (Union[Unset, None, int]):
        max_height (Union[Unset, None, int]):
        group_programs_by_series (Union[Unset, bool]):
        air_days (Union[Unset, List[DayOfWeek]]):
        is_airing (Union[Unset, None, bool]):
        has_aired (Union[Unset, None, bool]):
    """

    is_4k: Union[Unset, None, bool] = UNSET
    enable_total_record_count: Union[Unset, bool] = UNSET
    recording_keyword: Union[Unset, str] = UNSET
    recording_keyword_type: Union[Unset, LiveTvKeywordType] = UNSET
    random_seed: Union[Unset, int] = UNSET
    genre_ids: Union[Unset, str] = UNSET
    collection_ids: Union[Unset, str] = UNSET
    tag_ids: Union[Unset, str] = UNSET
    exclude_artist_ids: Union[Unset, str] = UNSET
    album_artist_ids: Union[Unset, str] = UNSET
    contributing_artist_ids: Union[Unset, str] = UNSET
    album_ids: Union[Unset, str] = UNSET
    outer_ids: Union[Unset, str] = UNSET
    list_item_ids: Union[Unset, str] = UNSET
    audio_languages: Union[Unset, str] = UNSET
    subtitle_languages: Union[Unset, str] = UNSET
    group_items_into: Union[Unset, LibraryItemLinkType] = UNSET
    min_width: Union[Unset, None, int] = UNSET
    min_height: Union[Unset, None, int] = UNSET
    max_width: Union[Unset, None, int] = UNSET
    max_height: Union[Unset, None, int] = UNSET
    group_programs_by_series: Union[Unset, bool] = UNSET
    air_days: Union[Unset, List[DayOfWeek]] = UNSET
    is_airing: Union[Unset, None, bool] = UNSET
    has_aired: Union[Unset, None, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_4k = self.is_4k
        enable_total_record_count = self.enable_total_record_count
        recording_keyword = self.recording_keyword
        recording_keyword_type: Union[Unset, str] = UNSET
        if not isinstance(self.recording_keyword_type, Unset):
            recording_keyword_type = self.recording_keyword_type.value

        random_seed = self.random_seed
        genre_ids = self.genre_ids
        collection_ids = self.collection_ids
        tag_ids = self.tag_ids
        exclude_artist_ids = self.exclude_artist_ids
        album_artist_ids = self.album_artist_ids
        contributing_artist_ids = self.contributing_artist_ids
        album_ids = self.album_ids
        outer_ids = self.outer_ids
        list_item_ids = self.list_item_ids
        audio_languages = self.audio_languages
        subtitle_languages = self.subtitle_languages
        group_items_into: Union[Unset, str] = UNSET
        if not isinstance(self.group_items_into, Unset):
            group_items_into = self.group_items_into.value

        min_width = self.min_width
        min_height = self.min_height
        max_width = self.max_width
        max_height = self.max_height
        group_programs_by_series = self.group_programs_by_series
        air_days: Union[Unset, List[str]] = UNSET
        if not isinstance(self.air_days, Unset):
            air_days = []
            for air_days_item_data in self.air_days:
                air_days_item = air_days_item_data.value

                air_days.append(air_days_item)

        is_airing = self.is_airing
        has_aired = self.has_aired

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_4k is not UNSET:
            field_dict["Is4K"] = is_4k
        if enable_total_record_count is not UNSET:
            field_dict["EnableTotalRecordCount"] = enable_total_record_count
        if recording_keyword is not UNSET:
            field_dict["RecordingKeyword"] = recording_keyword
        if recording_keyword_type is not UNSET:
            field_dict["RecordingKeywordType"] = recording_keyword_type
        if random_seed is not UNSET:
            field_dict["RandomSeed"] = random_seed
        if genre_ids is not UNSET:
            field_dict["GenreIds"] = genre_ids
        if collection_ids is not UNSET:
            field_dict["CollectionIds"] = collection_ids
        if tag_ids is not UNSET:
            field_dict["TagIds"] = tag_ids
        if exclude_artist_ids is not UNSET:
            field_dict["ExcludeArtistIds"] = exclude_artist_ids
        if album_artist_ids is not UNSET:
            field_dict["AlbumArtistIds"] = album_artist_ids
        if contributing_artist_ids is not UNSET:
            field_dict["ContributingArtistIds"] = contributing_artist_ids
        if album_ids is not UNSET:
            field_dict["AlbumIds"] = album_ids
        if outer_ids is not UNSET:
            field_dict["OuterIds"] = outer_ids
        if list_item_ids is not UNSET:
            field_dict["ListItemIds"] = list_item_ids
        if audio_languages is not UNSET:
            field_dict["AudioLanguages"] = audio_languages
        if subtitle_languages is not UNSET:
            field_dict["SubtitleLanguages"] = subtitle_languages
        if group_items_into is not UNSET:
            field_dict["GroupItemsInto"] = group_items_into
        if min_width is not UNSET:
            field_dict["MinWidth"] = min_width
        if min_height is not UNSET:
            field_dict["MinHeight"] = min_height
        if max_width is not UNSET:
            field_dict["MaxWidth"] = max_width
        if max_height is not UNSET:
            field_dict["MaxHeight"] = max_height
        if group_programs_by_series is not UNSET:
            field_dict["GroupProgramsBySeries"] = group_programs_by_series
        if air_days is not UNSET:
            field_dict["AirDays"] = air_days
        if is_airing is not UNSET:
            field_dict["IsAiring"] = is_airing
        if has_aired is not UNSET:
            field_dict["HasAired"] = has_aired

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_4k = d.pop("Is4K", UNSET)

        enable_total_record_count = d.pop("EnableTotalRecordCount", UNSET)

        recording_keyword = d.pop("RecordingKeyword", UNSET)

        _recording_keyword_type = d.pop("RecordingKeywordType", UNSET)
        recording_keyword_type: Union[Unset, LiveTvKeywordType]
        if isinstance(_recording_keyword_type, Unset):
            recording_keyword_type = UNSET
        else:
            recording_keyword_type = LiveTvKeywordType(_recording_keyword_type)

        random_seed = d.pop("RandomSeed", UNSET)

        genre_ids = d.pop("GenreIds", UNSET)

        collection_ids = d.pop("CollectionIds", UNSET)

        tag_ids = d.pop("TagIds", UNSET)

        exclude_artist_ids = d.pop("ExcludeArtistIds", UNSET)

        album_artist_ids = d.pop("AlbumArtistIds", UNSET)

        contributing_artist_ids = d.pop("ContributingArtistIds", UNSET)

        album_ids = d.pop("AlbumIds", UNSET)

        outer_ids = d.pop("OuterIds", UNSET)

        list_item_ids = d.pop("ListItemIds", UNSET)

        audio_languages = d.pop("AudioLanguages", UNSET)

        subtitle_languages = d.pop("SubtitleLanguages", UNSET)

        _group_items_into = d.pop("GroupItemsInto", UNSET)
        group_items_into: Union[Unset, LibraryItemLinkType]
        if isinstance(_group_items_into, Unset):
            group_items_into = UNSET
        else:
            group_items_into = LibraryItemLinkType(_group_items_into)

        min_width = d.pop("MinWidth", UNSET)

        min_height = d.pop("MinHeight", UNSET)

        max_width = d.pop("MaxWidth", UNSET)

        max_height = d.pop("MaxHeight", UNSET)

        group_programs_by_series = d.pop("GroupProgramsBySeries", UNSET)

        air_days = []
        _air_days = d.pop("AirDays", UNSET)
        for air_days_item_data in _air_days or []:
            air_days_item = DayOfWeek(air_days_item_data)

            air_days.append(air_days_item)

        is_airing = d.pop("IsAiring", UNSET)

        has_aired = d.pop("HasAired", UNSET)

        api_base_items_request = cls(
            is_4k=is_4k,
            enable_total_record_count=enable_total_record_count,
            recording_keyword=recording_keyword,
            recording_keyword_type=recording_keyword_type,
            random_seed=random_seed,
            genre_ids=genre_ids,
            collection_ids=collection_ids,
            tag_ids=tag_ids,
            exclude_artist_ids=exclude_artist_ids,
            album_artist_ids=album_artist_ids,
            contributing_artist_ids=contributing_artist_ids,
            album_ids=album_ids,
            outer_ids=outer_ids,
            list_item_ids=list_item_ids,
            audio_languages=audio_languages,
            subtitle_languages=subtitle_languages,
            group_items_into=group_items_into,
            min_width=min_width,
            min_height=min_height,
            max_width=max_width,
            max_height=max_height,
            group_programs_by_series=group_programs_by_series,
            air_days=air_days,
            is_airing=is_airing,
            has_aired=has_aired,
        )

        api_base_items_request.additional_properties = d
        return api_base_items_request

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
