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
    from ..models.provider_id_dictionary import ProviderIdDictionary


T = TypeVar("T", bound="LiveTvSeriesTimerInfo")


@attr.s(auto_attribs=True)
class LiveTvSeriesTimerInfo:
    """
    Attributes:
        id (Union[Unset, str]):
        channel_id (Union[Unset, str]):
        channel_ids (Union[Unset, List[str]]):
        program_id (Union[Unset, str]):
        name (Union[Unset, str]):
        service_name (Union[Unset, str]):
        overview (Union[Unset, str]):
        start_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):
        record_any_time (Union[Unset, bool]):
        keep_up_to (Union[Unset, int]):
        keep_until (Union[Unset, LiveTvKeepUntil]):
        skip_episodes_in_library (Union[Unset, bool]):
        record_new_only (Union[Unset, bool]):
        days (Union[Unset, List[DayOfWeek]]):
        priority (Union[Unset, int]):
        pre_padding_seconds (Union[Unset, int]):
        post_padding_seconds (Union[Unset, int]):
        is_pre_padding_required (Union[Unset, bool]):
        is_post_padding_required (Union[Unset, bool]):
        series_id (Union[Unset, str]):
        provider_ids (Union[Unset, ProviderIdDictionary]):
        max_recording_seconds (Union[Unset, int]):
        keywords (Union[Unset, List['LiveTvKeywordInfo']]):
        timer_type (Union[Unset, LiveTvTimerType]):
    """

    id: Union[Unset, str] = UNSET
    channel_id: Union[Unset, str] = UNSET
    channel_ids: Union[Unset, List[str]] = UNSET
    program_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    service_name: Union[Unset, str] = UNSET
    overview: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    record_any_time: Union[Unset, bool] = UNSET
    keep_up_to: Union[Unset, int] = UNSET
    keep_until: Union[Unset, LiveTvKeepUntil] = UNSET
    skip_episodes_in_library: Union[Unset, bool] = UNSET
    record_new_only: Union[Unset, bool] = UNSET
    days: Union[Unset, List[DayOfWeek]] = UNSET
    priority: Union[Unset, int] = UNSET
    pre_padding_seconds: Union[Unset, int] = UNSET
    post_padding_seconds: Union[Unset, int] = UNSET
    is_pre_padding_required: Union[Unset, bool] = UNSET
    is_post_padding_required: Union[Unset, bool] = UNSET
    series_id: Union[Unset, str] = UNSET
    provider_ids: Union[Unset, "ProviderIdDictionary"] = UNSET
    max_recording_seconds: Union[Unset, int] = UNSET
    keywords: Union[Unset, List["LiveTvKeywordInfo"]] = UNSET
    timer_type: Union[Unset, LiveTvTimerType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        channel_id = self.channel_id
        channel_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.channel_ids, Unset):
            channel_ids = self.channel_ids

        program_id = self.program_id
        name = self.name
        service_name = self.service_name
        overview = self.overview
        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        record_any_time = self.record_any_time
        keep_up_to = self.keep_up_to
        keep_until: Union[Unset, str] = UNSET
        if not isinstance(self.keep_until, Unset):
            keep_until = self.keep_until.value

        skip_episodes_in_library = self.skip_episodes_in_library
        record_new_only = self.record_new_only
        days: Union[Unset, List[str]] = UNSET
        if not isinstance(self.days, Unset):
            days = []
            for days_item_data in self.days:
                days_item = days_item_data.value

                days.append(days_item)

        priority = self.priority
        pre_padding_seconds = self.pre_padding_seconds
        post_padding_seconds = self.post_padding_seconds
        is_pre_padding_required = self.is_pre_padding_required
        is_post_padding_required = self.is_post_padding_required
        series_id = self.series_id
        provider_ids: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.provider_ids, Unset):
            provider_ids = self.provider_ids.to_dict()

        max_recording_seconds = self.max_recording_seconds
        keywords: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.keywords, Unset):
            keywords = []
            for keywords_item_data in self.keywords:
                keywords_item = keywords_item_data.to_dict()

                keywords.append(keywords_item)

        timer_type: Union[Unset, str] = UNSET
        if not isinstance(self.timer_type, Unset):
            timer_type = self.timer_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if channel_id is not UNSET:
            field_dict["ChannelId"] = channel_id
        if channel_ids is not UNSET:
            field_dict["ChannelIds"] = channel_ids
        if program_id is not UNSET:
            field_dict["ProgramId"] = program_id
        if name is not UNSET:
            field_dict["Name"] = name
        if service_name is not UNSET:
            field_dict["ServiceName"] = service_name
        if overview is not UNSET:
            field_dict["Overview"] = overview
        if start_date is not UNSET:
            field_dict["StartDate"] = start_date
        if end_date is not UNSET:
            field_dict["EndDate"] = end_date
        if record_any_time is not UNSET:
            field_dict["RecordAnyTime"] = record_any_time
        if keep_up_to is not UNSET:
            field_dict["KeepUpTo"] = keep_up_to
        if keep_until is not UNSET:
            field_dict["KeepUntil"] = keep_until
        if skip_episodes_in_library is not UNSET:
            field_dict["SkipEpisodesInLibrary"] = skip_episodes_in_library
        if record_new_only is not UNSET:
            field_dict["RecordNewOnly"] = record_new_only
        if days is not UNSET:
            field_dict["Days"] = days
        if priority is not UNSET:
            field_dict["Priority"] = priority
        if pre_padding_seconds is not UNSET:
            field_dict["PrePaddingSeconds"] = pre_padding_seconds
        if post_padding_seconds is not UNSET:
            field_dict["PostPaddingSeconds"] = post_padding_seconds
        if is_pre_padding_required is not UNSET:
            field_dict["IsPrePaddingRequired"] = is_pre_padding_required
        if is_post_padding_required is not UNSET:
            field_dict["IsPostPaddingRequired"] = is_post_padding_required
        if series_id is not UNSET:
            field_dict["SeriesId"] = series_id
        if provider_ids is not UNSET:
            field_dict["ProviderIds"] = provider_ids
        if max_recording_seconds is not UNSET:
            field_dict["MaxRecordingSeconds"] = max_recording_seconds
        if keywords is not UNSET:
            field_dict["Keywords"] = keywords
        if timer_type is not UNSET:
            field_dict["TimerType"] = timer_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.live_tv_keyword_info import LiveTvKeywordInfo
        from ..models.provider_id_dictionary import ProviderIdDictionary

        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        channel_id = d.pop("ChannelId", UNSET)

        channel_ids = cast(List[str], d.pop("ChannelIds", UNSET))

        program_id = d.pop("ProgramId", UNSET)

        name = d.pop("Name", UNSET)

        service_name = d.pop("ServiceName", UNSET)

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

        record_any_time = d.pop("RecordAnyTime", UNSET)

        keep_up_to = d.pop("KeepUpTo", UNSET)

        _keep_until = d.pop("KeepUntil", UNSET)
        keep_until: Union[Unset, LiveTvKeepUntil]
        if isinstance(_keep_until, Unset):
            keep_until = UNSET
        else:
            keep_until = LiveTvKeepUntil(_keep_until)

        skip_episodes_in_library = d.pop("SkipEpisodesInLibrary", UNSET)

        record_new_only = d.pop("RecordNewOnly", UNSET)

        days = []
        _days = d.pop("Days", UNSET)
        for days_item_data in _days or []:
            days_item = DayOfWeek(days_item_data)

            days.append(days_item)

        priority = d.pop("Priority", UNSET)

        pre_padding_seconds = d.pop("PrePaddingSeconds", UNSET)

        post_padding_seconds = d.pop("PostPaddingSeconds", UNSET)

        is_pre_padding_required = d.pop("IsPrePaddingRequired", UNSET)

        is_post_padding_required = d.pop("IsPostPaddingRequired", UNSET)

        series_id = d.pop("SeriesId", UNSET)

        _provider_ids = d.pop("ProviderIds", UNSET)
        provider_ids: Union[Unset, ProviderIdDictionary]
        if isinstance(_provider_ids, Unset):
            provider_ids = UNSET
        else:
            provider_ids = ProviderIdDictionary.from_dict(_provider_ids)

        max_recording_seconds = d.pop("MaxRecordingSeconds", UNSET)

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

        live_tv_series_timer_info = cls(
            id=id,
            channel_id=channel_id,
            channel_ids=channel_ids,
            program_id=program_id,
            name=name,
            service_name=service_name,
            overview=overview,
            start_date=start_date,
            end_date=end_date,
            record_any_time=record_any_time,
            keep_up_to=keep_up_to,
            keep_until=keep_until,
            skip_episodes_in_library=skip_episodes_in_library,
            record_new_only=record_new_only,
            days=days,
            priority=priority,
            pre_padding_seconds=pre_padding_seconds,
            post_padding_seconds=post_padding_seconds,
            is_pre_padding_required=is_pre_padding_required,
            is_post_padding_required=is_post_padding_required,
            series_id=series_id,
            provider_ids=provider_ids,
            max_recording_seconds=max_recording_seconds,
            keywords=keywords,
            timer_type=timer_type,
        )

        live_tv_series_timer_info.additional_properties = d
        return live_tv_series_timer_info

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
