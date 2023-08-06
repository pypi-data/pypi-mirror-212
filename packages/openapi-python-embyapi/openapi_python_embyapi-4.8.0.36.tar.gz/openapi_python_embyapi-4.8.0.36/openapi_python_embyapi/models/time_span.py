from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeSpan")


@attr.s(auto_attribs=True)
class TimeSpan:
    """
    Attributes:
        ticks (Union[Unset, int]):
        days (Union[Unset, int]):
        hours (Union[Unset, int]):
        milliseconds (Union[Unset, int]):
        minutes (Union[Unset, int]):
        seconds (Union[Unset, int]):
        total_days (Union[Unset, float]):
        total_hours (Union[Unset, float]):
        total_milliseconds (Union[Unset, float]):
        total_minutes (Union[Unset, float]):
        total_seconds (Union[Unset, float]):
    """

    ticks: Union[Unset, int] = UNSET
    days: Union[Unset, int] = UNSET
    hours: Union[Unset, int] = UNSET
    milliseconds: Union[Unset, int] = UNSET
    minutes: Union[Unset, int] = UNSET
    seconds: Union[Unset, int] = UNSET
    total_days: Union[Unset, float] = UNSET
    total_hours: Union[Unset, float] = UNSET
    total_milliseconds: Union[Unset, float] = UNSET
    total_minutes: Union[Unset, float] = UNSET
    total_seconds: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        ticks = self.ticks
        days = self.days
        hours = self.hours
        milliseconds = self.milliseconds
        minutes = self.minutes
        seconds = self.seconds
        total_days = self.total_days
        total_hours = self.total_hours
        total_milliseconds = self.total_milliseconds
        total_minutes = self.total_minutes
        total_seconds = self.total_seconds

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ticks is not UNSET:
            field_dict["Ticks"] = ticks
        if days is not UNSET:
            field_dict["Days"] = days
        if hours is not UNSET:
            field_dict["Hours"] = hours
        if milliseconds is not UNSET:
            field_dict["Milliseconds"] = milliseconds
        if minutes is not UNSET:
            field_dict["Minutes"] = minutes
        if seconds is not UNSET:
            field_dict["Seconds"] = seconds
        if total_days is not UNSET:
            field_dict["TotalDays"] = total_days
        if total_hours is not UNSET:
            field_dict["TotalHours"] = total_hours
        if total_milliseconds is not UNSET:
            field_dict["TotalMilliseconds"] = total_milliseconds
        if total_minutes is not UNSET:
            field_dict["TotalMinutes"] = total_minutes
        if total_seconds is not UNSET:
            field_dict["TotalSeconds"] = total_seconds

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ticks = d.pop("Ticks", UNSET)

        days = d.pop("Days", UNSET)

        hours = d.pop("Hours", UNSET)

        milliseconds = d.pop("Milliseconds", UNSET)

        minutes = d.pop("Minutes", UNSET)

        seconds = d.pop("Seconds", UNSET)

        total_days = d.pop("TotalDays", UNSET)

        total_hours = d.pop("TotalHours", UNSET)

        total_milliseconds = d.pop("TotalMilliseconds", UNSET)

        total_minutes = d.pop("TotalMinutes", UNSET)

        total_seconds = d.pop("TotalSeconds", UNSET)

        time_span = cls(
            ticks=ticks,
            days=days,
            hours=hours,
            milliseconds=milliseconds,
            minutes=minutes,
            seconds=seconds,
            total_days=total_days,
            total_hours=total_hours,
            total_milliseconds=total_milliseconds,
            total_minutes=total_minutes,
            total_seconds=total_seconds,
        )

        time_span.additional_properties = d
        return time_span

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
