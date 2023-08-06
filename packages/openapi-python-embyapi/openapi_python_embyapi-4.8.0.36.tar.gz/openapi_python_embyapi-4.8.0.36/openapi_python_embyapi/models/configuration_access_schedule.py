from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.configuration_dynamic_day_of_week import ConfigurationDynamicDayOfWeek
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConfigurationAccessSchedule")


@attr.s(auto_attribs=True)
class ConfigurationAccessSchedule:
    """
    Attributes:
        day_of_week (Union[Unset, ConfigurationDynamicDayOfWeek]):
        start_hour (Union[Unset, float]):
        end_hour (Union[Unset, float]):
    """

    day_of_week: Union[Unset, ConfigurationDynamicDayOfWeek] = UNSET
    start_hour: Union[Unset, float] = UNSET
    end_hour: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        day_of_week: Union[Unset, str] = UNSET
        if not isinstance(self.day_of_week, Unset):
            day_of_week = self.day_of_week.value

        start_hour = self.start_hour
        end_hour = self.end_hour

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if day_of_week is not UNSET:
            field_dict["DayOfWeek"] = day_of_week
        if start_hour is not UNSET:
            field_dict["StartHour"] = start_hour
        if end_hour is not UNSET:
            field_dict["EndHour"] = end_hour

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _day_of_week = d.pop("DayOfWeek", UNSET)
        day_of_week: Union[Unset, ConfigurationDynamicDayOfWeek]
        if isinstance(_day_of_week, Unset):
            day_of_week = UNSET
        else:
            day_of_week = ConfigurationDynamicDayOfWeek(_day_of_week)

        start_hour = d.pop("StartHour", UNSET)

        end_hour = d.pop("EndHour", UNSET)

        configuration_access_schedule = cls(
            day_of_week=day_of_week,
            start_hour=start_hour,
            end_hour=end_hour,
        )

        configuration_access_schedule.additional_properties = d
        return configuration_access_schedule

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
