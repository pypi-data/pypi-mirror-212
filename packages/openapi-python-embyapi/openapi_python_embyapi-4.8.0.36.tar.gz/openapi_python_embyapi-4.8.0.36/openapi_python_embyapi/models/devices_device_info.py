import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DevicesDeviceInfo")


@attr.s(auto_attribs=True)
class DevicesDeviceInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        id (Union[Unset, str]):
        internal_id (Union[Unset, int]):
        reported_device_id (Union[Unset, str]):
        last_user_name (Union[Unset, str]):
        app_name (Union[Unset, str]):
        app_version (Union[Unset, str]):
        last_user_id (Union[Unset, str]):
        date_last_activity (Union[Unset, datetime.datetime]):
        icon_url (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    internal_id: Union[Unset, int] = UNSET
    reported_device_id: Union[Unset, str] = UNSET
    last_user_name: Union[Unset, str] = UNSET
    app_name: Union[Unset, str] = UNSET
    app_version: Union[Unset, str] = UNSET
    last_user_id: Union[Unset, str] = UNSET
    date_last_activity: Union[Unset, datetime.datetime] = UNSET
    icon_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        internal_id = self.internal_id
        reported_device_id = self.reported_device_id
        last_user_name = self.last_user_name
        app_name = self.app_name
        app_version = self.app_version
        last_user_id = self.last_user_id
        date_last_activity: Union[Unset, str] = UNSET
        if not isinstance(self.date_last_activity, Unset):
            date_last_activity = self.date_last_activity.isoformat()

        icon_url = self.icon_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if id is not UNSET:
            field_dict["Id"] = id
        if internal_id is not UNSET:
            field_dict["InternalId"] = internal_id
        if reported_device_id is not UNSET:
            field_dict["ReportedDeviceId"] = reported_device_id
        if last_user_name is not UNSET:
            field_dict["LastUserName"] = last_user_name
        if app_name is not UNSET:
            field_dict["AppName"] = app_name
        if app_version is not UNSET:
            field_dict["AppVersion"] = app_version
        if last_user_id is not UNSET:
            field_dict["LastUserId"] = last_user_id
        if date_last_activity is not UNSET:
            field_dict["DateLastActivity"] = date_last_activity
        if icon_url is not UNSET:
            field_dict["IconUrl"] = icon_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        id = d.pop("Id", UNSET)

        internal_id = d.pop("InternalId", UNSET)

        reported_device_id = d.pop("ReportedDeviceId", UNSET)

        last_user_name = d.pop("LastUserName", UNSET)

        app_name = d.pop("AppName", UNSET)

        app_version = d.pop("AppVersion", UNSET)

        last_user_id = d.pop("LastUserId", UNSET)

        _date_last_activity = d.pop("DateLastActivity", UNSET)
        date_last_activity: Union[Unset, datetime.datetime]
        if isinstance(_date_last_activity, Unset):
            date_last_activity = UNSET
        else:
            date_last_activity = isoparse(_date_last_activity)

        icon_url = d.pop("IconUrl", UNSET)

        devices_device_info = cls(
            name=name,
            id=id,
            internal_id=internal_id,
            reported_device_id=reported_device_id,
            last_user_name=last_user_name,
            app_name=app_name,
            app_version=app_version,
            last_user_id=last_user_id,
            date_last_activity=date_last_activity,
            icon_url=icon_url,
        )

        devices_device_info.additional_properties = d
        return devices_device_info

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
