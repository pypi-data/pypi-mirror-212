import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.live_tv_keep_until import LiveTvKeepUntil
from ..models.live_tv_recording_status import LiveTvRecordingStatus
from ..models.live_tv_timer_type import LiveTvTimerType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_item_dto import BaseItemDto


T = TypeVar("T", bound="LiveTvTimerInfoDto")


@attr.s(auto_attribs=True)
class LiveTvTimerInfoDto:
    """
    Attributes:
        status (Union[Unset, LiveTvRecordingStatus]):
        series_timer_id (Union[Unset, str]):
        run_time_ticks (Union[Unset, None, int]):
        program_info (Union[Unset, BaseItemDto]):
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

    status: Union[Unset, LiveTvRecordingStatus] = UNSET
    series_timer_id: Union[Unset, str] = UNSET
    run_time_ticks: Union[Unset, None, int] = UNSET
    program_info: Union[Unset, "BaseItemDto"] = UNSET
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
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        series_timer_id = self.series_timer_id
        run_time_ticks = self.run_time_ticks
        program_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.program_info, Unset):
            program_info = self.program_info.to_dict()

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
        if status is not UNSET:
            field_dict["Status"] = status
        if series_timer_id is not UNSET:
            field_dict["SeriesTimerId"] = series_timer_id
        if run_time_ticks is not UNSET:
            field_dict["RunTimeTicks"] = run_time_ticks
        if program_info is not UNSET:
            field_dict["ProgramInfo"] = program_info
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
        from ..models.base_item_dto import BaseItemDto

        d = src_dict.copy()
        _status = d.pop("Status", UNSET)
        status: Union[Unset, LiveTvRecordingStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = LiveTvRecordingStatus(_status)

        series_timer_id = d.pop("SeriesTimerId", UNSET)

        run_time_ticks = d.pop("RunTimeTicks", UNSET)

        _program_info = d.pop("ProgramInfo", UNSET)
        program_info: Union[Unset, BaseItemDto]
        if isinstance(_program_info, Unset):
            program_info = UNSET
        else:
            program_info = BaseItemDto.from_dict(_program_info)

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

        live_tv_timer_info_dto = cls(
            status=status,
            series_timer_id=series_timer_id,
            run_time_ticks=run_time_ticks,
            program_info=program_info,
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

        live_tv_timer_info_dto.additional_properties = d
        return live_tv_timer_info_dto

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
