import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.logging_log_severity import LoggingLogSeverity
from ..types import UNSET, Unset

T = TypeVar("T", bound="ActivityLogEntry")


@attr.s(auto_attribs=True)
class ActivityLogEntry:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]):
        overview (Union[Unset, str]):
        short_overview (Union[Unset, str]):
        type (Union[Unset, str]):
        item_id (Union[Unset, str]):
        date (Union[Unset, datetime.datetime]):
        user_id (Union[Unset, str]):
        user_primary_image_tag (Union[Unset, str]):
        severity (Union[Unset, LoggingLogSeverity]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    overview: Union[Unset, str] = UNSET
    short_overview: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    item_id: Union[Unset, str] = UNSET
    date: Union[Unset, datetime.datetime] = UNSET
    user_id: Union[Unset, str] = UNSET
    user_primary_image_tag: Union[Unset, str] = UNSET
    severity: Union[Unset, LoggingLogSeverity] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        overview = self.overview
        short_overview = self.short_overview
        type = self.type
        item_id = self.item_id
        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        user_id = self.user_id
        user_primary_image_tag = self.user_primary_image_tag
        severity: Union[Unset, str] = UNSET
        if not isinstance(self.severity, Unset):
            severity = self.severity.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if name is not UNSET:
            field_dict["Name"] = name
        if overview is not UNSET:
            field_dict["Overview"] = overview
        if short_overview is not UNSET:
            field_dict["ShortOverview"] = short_overview
        if type is not UNSET:
            field_dict["Type"] = type
        if item_id is not UNSET:
            field_dict["ItemId"] = item_id
        if date is not UNSET:
            field_dict["Date"] = date
        if user_id is not UNSET:
            field_dict["UserId"] = user_id
        if user_primary_image_tag is not UNSET:
            field_dict["UserPrimaryImageTag"] = user_primary_image_tag
        if severity is not UNSET:
            field_dict["Severity"] = severity

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        name = d.pop("Name", UNSET)

        overview = d.pop("Overview", UNSET)

        short_overview = d.pop("ShortOverview", UNSET)

        type = d.pop("Type", UNSET)

        item_id = d.pop("ItemId", UNSET)

        _date = d.pop("Date", UNSET)
        date: Union[Unset, datetime.datetime]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date)

        user_id = d.pop("UserId", UNSET)

        user_primary_image_tag = d.pop("UserPrimaryImageTag", UNSET)

        _severity = d.pop("Severity", UNSET)
        severity: Union[Unset, LoggingLogSeverity]
        if isinstance(_severity, Unset):
            severity = UNSET
        else:
            severity = LoggingLogSeverity(_severity)

        activity_log_entry = cls(
            id=id,
            name=name,
            overview=overview,
            short_overview=short_overview,
            type=type,
            item_id=item_id,
            date=date,
            user_id=user_id,
            user_primary_image_tag=user_primary_image_tag,
            severity=severity,
        )

        activity_log_entry.additional_properties = d
        return activity_log_entry

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
