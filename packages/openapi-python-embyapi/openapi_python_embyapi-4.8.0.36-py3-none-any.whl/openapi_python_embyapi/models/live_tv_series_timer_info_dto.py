import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.day_of_week import DayOfWeek
from ..models.live_tv_keep_until import LiveTvKeepUntil
from ..models.live_tv_timer_type import LiveTvTimerType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.live_tv_keyword_info import LiveTvKeywordInfo
    from ..models.live_tv_series_timer_info_dto_image_tags import LiveTvSeriesTimerInfoDtoImageTags


T = TypeVar("T", bound="LiveTvSeriesTimerInfoDto")


@attr.s(auto_attribs=True)
class LiveTvSeriesTimerInfoDto:
    """
    Attributes:
        record_any_time (Union[Unset, bool]):
        skip_episodes_in_library (Union[Unset, bool]):
        record_any_channel (Union[Unset, bool]):
        keep_up_to (Union[Unset, int]):
        max_recording_seconds (Union[Unset, int]):
        record_new_only (Union[Unset, bool]):
        channel_ids (Union[Unset, List[str]]):
        days (Union[Unset, List[DayOfWeek]]):
        image_tags (Union[Unset, LiveTvSeriesTimerInfoDtoImageTags]):
        parent_thumb_item_id (Union[Unset, str]):
        parent_thumb_image_tag (Union[Unset, str]):
        parent_primary_image_item_id (Union[Unset, str]):
        parent_primary_image_tag (Union[Unset, str]):
        series_id (Union[Unset, str]):
        keywords (Union[Unset, List['LiveTvKeywordInfo']]):
        timer_type (Union[Unset, LiveTvTimerType]):
        id (Union[Unset, str]):
        type (Union[Unset, str]):
        server_id (Union[Unset, str]):
        channel_id (Union[Unset, str]):
        channel_name (Union[Unset, str]):
        channel_number (Union[Unset, str]):
        channel_primary_image_tag (Union[Unset, str]):
        program_id (Union[Unset, str]):
        name (Union[Unset, str]):
        overview (Union[Unset, str]):
        start_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):
        priority (Union[Unset, int]):
        pre_padding_seconds (Union[Unset, int]):
        post_padding_seconds (Union[Unset, int]):
        is_pre_padding_required (Union[Unset, bool]):
        parent_backdrop_item_id (Union[Unset, str]):
        parent_backdrop_image_tags (Union[Unset, List[str]]):
        is_post_padding_required (Union[Unset, bool]):
        keep_until (Union[Unset, LiveTvKeepUntil]):
    """

    record_any_time: Union[Unset, bool] = UNSET
    skip_episodes_in_library: Union[Unset, bool] = UNSET
    record_any_channel: Union[Unset, bool] = UNSET
    keep_up_to: Union[Unset, int] = UNSET
    max_recording_seconds: Union[Unset, int] = UNSET
    record_new_only: Union[Unset, bool] = UNSET
    channel_ids: Union[Unset, List[str]] = UNSET
    days: Union[Unset, List[DayOfWeek]] = UNSET
    image_tags: Union[Unset, "LiveTvSeriesTimerInfoDtoImageTags"] = UNSET
    parent_thumb_item_id: Union[Unset, str] = UNSET
    parent_thumb_image_tag: Union[Unset, str] = UNSET
    parent_primary_image_item_id: Union[Unset, str] = UNSET
    parent_primary_image_tag: Union[Unset, str] = UNSET
    series_id: Union[Unset, str] = UNSET
    keywords: Union[Unset, List["LiveTvKeywordInfo"]] = UNSET
    timer_type: Union[Unset, LiveTvTimerType] = UNSET
    id: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    server_id: Union[Unset, str] = UNSET
    channel_id: Union[Unset, str] = UNSET
    channel_name: Union[Unset, str] = UNSET
    channel_number: Union[Unset, str] = UNSET
    channel_primary_image_tag: Union[Unset, str] = UNSET
    program_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    overview: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    priority: Union[Unset, int] = UNSET
    pre_padding_seconds: Union[Unset, int] = UNSET
    post_padding_seconds: Union[Unset, int] = UNSET
    is_pre_padding_required: Union[Unset, bool] = UNSET
    parent_backdrop_item_id: Union[Unset, str] = UNSET
    parent_backdrop_image_tags: Union[Unset, List[str]] = UNSET
    is_post_padding_required: Union[Unset, bool] = UNSET
    keep_until: Union[Unset, LiveTvKeepUntil] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        record_any_time = self.record_any_time
        skip_episodes_in_library = self.skip_episodes_in_library
        record_any_channel = self.record_any_channel
        keep_up_to = self.keep_up_to
        max_recording_seconds = self.max_recording_seconds
        record_new_only = self.record_new_only
        channel_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.channel_ids, Unset):
            channel_ids = self.channel_ids

        days: Union[Unset, List[str]] = UNSET
        if not isinstance(self.days, Unset):
            days = []
            for days_item_data in self.days:
                days_item = days_item_data.value

                days.append(days_item)

        image_tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.image_tags, Unset):
            image_tags = self.image_tags.to_dict()

        parent_thumb_item_id = self.parent_thumb_item_id
        parent_thumb_image_tag = self.parent_thumb_image_tag
        parent_primary_image_item_id = self.parent_primary_image_item_id
        parent_primary_image_tag = self.parent_primary_image_tag
        series_id = self.series_id
        keywords: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.keywords, Unset):
            keywords = []
            for keywords_item_data in self.keywords:
                keywords_item = keywords_item_data.to_dict()

                keywords.append(keywords_item)

        timer_type: Union[Unset, str] = UNSET
        if not isinstance(self.timer_type, Unset):
            timer_type = self.timer_type.value

        id = self.id
        type = self.type
        server_id = self.server_id
        channel_id = self.channel_id
        channel_name = self.channel_name
        channel_number = self.channel_number
        channel_primary_image_tag = self.channel_primary_image_tag
        program_id = self.program_id
        name = self.name
        overview = self.overview
        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        priority = self.priority
        pre_padding_seconds = self.pre_padding_seconds
        post_padding_seconds = self.post_padding_seconds
        is_pre_padding_required = self.is_pre_padding_required
        parent_backdrop_item_id = self.parent_backdrop_item_id
        parent_backdrop_image_tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.parent_backdrop_image_tags, Unset):
            parent_backdrop_image_tags = self.parent_backdrop_image_tags

        is_post_padding_required = self.is_post_padding_required
        keep_until: Union[Unset, str] = UNSET
        if not isinstance(self.keep_until, Unset):
            keep_until = self.keep_until.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if record_any_time is not UNSET:
            field_dict["RecordAnyTime"] = record_any_time
        if skip_episodes_in_library is not UNSET:
            field_dict["SkipEpisodesInLibrary"] = skip_episodes_in_library
        if record_any_channel is not UNSET:
            field_dict["RecordAnyChannel"] = record_any_channel
        if keep_up_to is not UNSET:
            field_dict["KeepUpTo"] = keep_up_to
        if max_recording_seconds is not UNSET:
            field_dict["MaxRecordingSeconds"] = max_recording_seconds
        if record_new_only is not UNSET:
            field_dict["RecordNewOnly"] = record_new_only
        if channel_ids is not UNSET:
            field_dict["ChannelIds"] = channel_ids
        if days is not UNSET:
            field_dict["Days"] = days
        if image_tags is not UNSET:
            field_dict["ImageTags"] = image_tags
        if parent_thumb_item_id is not UNSET:
            field_dict["ParentThumbItemId"] = parent_thumb_item_id
        if parent_thumb_image_tag is not UNSET:
            field_dict["ParentThumbImageTag"] = parent_thumb_image_tag
        if parent_primary_image_item_id is not UNSET:
            field_dict["ParentPrimaryImageItemId"] = parent_primary_image_item_id
        if parent_primary_image_tag is not UNSET:
            field_dict["ParentPrimaryImageTag"] = parent_primary_image_tag
        if series_id is not UNSET:
            field_dict["SeriesId"] = series_id
        if keywords is not UNSET:
            field_dict["Keywords"] = keywords
        if timer_type is not UNSET:
            field_dict["TimerType"] = timer_type
        if id is not UNSET:
            field_dict["Id"] = id
        if type is not UNSET:
            field_dict["Type"] = type
        if server_id is not UNSET:
            field_dict["ServerId"] = server_id
        if channel_id is not UNSET:
            field_dict["ChannelId"] = channel_id
        if channel_name is not UNSET:
            field_dict["ChannelName"] = channel_name
        if channel_number is not UNSET:
            field_dict["ChannelNumber"] = channel_number
        if channel_primary_image_tag is not UNSET:
            field_dict["ChannelPrimaryImageTag"] = channel_primary_image_tag
        if program_id is not UNSET:
            field_dict["ProgramId"] = program_id
        if name is not UNSET:
            field_dict["Name"] = name
        if overview is not UNSET:
            field_dict["Overview"] = overview
        if start_date is not UNSET:
            field_dict["StartDate"] = start_date
        if end_date is not UNSET:
            field_dict["EndDate"] = end_date
        if priority is not UNSET:
            field_dict["Priority"] = priority
        if pre_padding_seconds is not UNSET:
            field_dict["PrePaddingSeconds"] = pre_padding_seconds
        if post_padding_seconds is not UNSET:
            field_dict["PostPaddingSeconds"] = post_padding_seconds
        if is_pre_padding_required is not UNSET:
            field_dict["IsPrePaddingRequired"] = is_pre_padding_required
        if parent_backdrop_item_id is not UNSET:
            field_dict["ParentBackdropItemId"] = parent_backdrop_item_id
        if parent_backdrop_image_tags is not UNSET:
            field_dict["ParentBackdropImageTags"] = parent_backdrop_image_tags
        if is_post_padding_required is not UNSET:
            field_dict["IsPostPaddingRequired"] = is_post_padding_required
        if keep_until is not UNSET:
            field_dict["KeepUntil"] = keep_until

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.live_tv_keyword_info import LiveTvKeywordInfo
        from ..models.live_tv_series_timer_info_dto_image_tags import LiveTvSeriesTimerInfoDtoImageTags

        d = src_dict.copy()
        record_any_time = d.pop("RecordAnyTime", UNSET)

        skip_episodes_in_library = d.pop("SkipEpisodesInLibrary", UNSET)

        record_any_channel = d.pop("RecordAnyChannel", UNSET)

        keep_up_to = d.pop("KeepUpTo", UNSET)

        max_recording_seconds = d.pop("MaxRecordingSeconds", UNSET)

        record_new_only = d.pop("RecordNewOnly", UNSET)

        channel_ids = cast(List[str], d.pop("ChannelIds", UNSET))

        days = []
        _days = d.pop("Days", UNSET)
        for days_item_data in _days or []:
            days_item = DayOfWeek(days_item_data)

            days.append(days_item)

        _image_tags = d.pop("ImageTags", UNSET)
        image_tags: Union[Unset, LiveTvSeriesTimerInfoDtoImageTags]
        if isinstance(_image_tags, Unset):
            image_tags = UNSET
        else:
            image_tags = LiveTvSeriesTimerInfoDtoImageTags.from_dict(_image_tags)

        parent_thumb_item_id = d.pop("ParentThumbItemId", UNSET)

        parent_thumb_image_tag = d.pop("ParentThumbImageTag", UNSET)

        parent_primary_image_item_id = d.pop("ParentPrimaryImageItemId", UNSET)

        parent_primary_image_tag = d.pop("ParentPrimaryImageTag", UNSET)

        series_id = d.pop("SeriesId", UNSET)

        keywords = []
        _keywords = d.pop("Keywords", UNSET)
        for keywords_item_data in _keywords or []:
            keywords_item = LiveTvKeywordInfo.from_dict(keywords_item_data)

            keywords.append(keywords_item)

        _timer_type = d.pop("TimerType", UNSET)
        timer_type: Union[Unset, LiveTvTimerType]
        if isinstance(_timer_type, Unset):
            timer_type = UNSET
        else:
            timer_type = LiveTvTimerType(_timer_type)

        id = d.pop("Id", UNSET)

        type = d.pop("Type", UNSET)

        server_id = d.pop("ServerId", UNSET)

        channel_id = d.pop("ChannelId", UNSET)

        channel_name = d.pop("ChannelName", UNSET)

        channel_number = d.pop("ChannelNumber", UNSET)

        channel_primary_image_tag = d.pop("ChannelPrimaryImageTag", UNSET)

        program_id = d.pop("ProgramId", UNSET)

        name = d.pop("Name", UNSET)

        overview = d.pop("Overview", UNSET)

        _start_date = d.pop("StartDate", UNSET)
        start_date: Union[Unset, datetime.datetime]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date)

        _end_date = d.pop("EndDate", UNSET)
        end_date: Union[Unset, datetime.datetime]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date)

        priority = d.pop("Priority", UNSET)

        pre_padding_seconds = d.pop("PrePaddingSeconds", UNSET)

        post_padding_seconds = d.pop("PostPaddingSeconds", UNSET)

        is_pre_padding_required = d.pop("IsPrePaddingRequired", UNSET)

        parent_backdrop_item_id = d.pop("ParentBackdropItemId", UNSET)

        parent_backdrop_image_tags = cast(List[str], d.pop("ParentBackdropImageTags", UNSET))

        is_post_padding_required = d.pop("IsPostPaddingRequired", UNSET)

        _keep_until = d.pop("KeepUntil", UNSET)
        keep_until: Union[Unset, LiveTvKeepUntil]
        if isinstance(_keep_until, Unset):
            keep_until = UNSET
        else:
            keep_until = LiveTvKeepUntil(_keep_until)

        live_tv_series_timer_info_dto = cls(
            record_any_time=record_any_time,
            skip_episodes_in_library=skip_episodes_in_library,
            record_any_channel=record_any_channel,
            keep_up_to=keep_up_to,
            max_recording_seconds=max_recording_seconds,
            record_new_only=record_new_only,
            channel_ids=channel_ids,
            days=days,
            image_tags=image_tags,
            parent_thumb_item_id=parent_thumb_item_id,
            parent_thumb_image_tag=parent_thumb_image_tag,
            parent_primary_image_item_id=parent_primary_image_item_id,
            parent_primary_image_tag=parent_primary_image_tag,
            series_id=series_id,
            keywords=keywords,
            timer_type=timer_type,
            id=id,
            type=type,
            server_id=server_id,
            channel_id=channel_id,
            channel_name=channel_name,
            channel_number=channel_number,
            channel_primary_image_tag=channel_primary_image_tag,
            program_id=program_id,
            name=name,
            overview=overview,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            pre_padding_seconds=pre_padding_seconds,
            post_padding_seconds=post_padding_seconds,
            is_pre_padding_required=is_pre_padding_required,
            parent_backdrop_item_id=parent_backdrop_item_id,
            parent_backdrop_image_tags=parent_backdrop_image_tags,
            is_post_padding_required=is_post_padding_required,
            keep_until=keep_until,
        )

        live_tv_series_timer_info_dto.additional_properties = d
        return live_tv_series_timer_info_dto

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
