from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.day_of_week import DayOfWeek
from ..models.tasks_system_event import TasksSystemEvent
from ..types import UNSET, Unset

T = TypeVar("T", bound="TasksTaskTriggerInfo")


@attr.s(auto_attribs=True)
class TasksTaskTriggerInfo:
    """
    Attributes:
        type (Union[Unset, str]):
        time_of_day_ticks (Union[Unset, None, int]):
        interval_ticks (Union[Unset, None, int]):
        system_event (Union[Unset, TasksSystemEvent]):
        day_of_week (Union[Unset, DayOfWeek]):
        max_runtime_ticks (Union[Unset, None, int]):
    """

    type: Union[Unset, str] = UNSET
    time_of_day_ticks: Union[Unset, None, int] = UNSET
    interval_ticks: Union[Unset, None, int] = UNSET
    system_event: Union[Unset, TasksSystemEvent] = UNSET
    day_of_week: Union[Unset, DayOfWeek] = UNSET
    max_runtime_ticks: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        time_of_day_ticks = self.time_of_day_ticks
        interval_ticks = self.interval_ticks
        system_event: Union[Unset, str] = UNSET
        if not isinstance(self.system_event, Unset):
            system_event = self.system_event.value

        day_of_week: Union[Unset, str] = UNSET
        if not isinstance(self.day_of_week, Unset):
            day_of_week = self.day_of_week.value

        max_runtime_ticks = self.max_runtime_ticks

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["Type"] = type
        if time_of_day_ticks is not UNSET:
            field_dict["TimeOfDayTicks"] = time_of_day_ticks
        if interval_ticks is not UNSET:
            field_dict["IntervalTicks"] = interval_ticks
        if system_event is not UNSET:
            field_dict["SystemEvent"] = system_event
        if day_of_week is not UNSET:
            field_dict["DayOfWeek"] = day_of_week
        if max_runtime_ticks is not UNSET:
            field_dict["MaxRuntimeTicks"] = max_runtime_ticks

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("Type", UNSET)

        time_of_day_ticks = d.pop("TimeOfDayTicks", UNSET)

        interval_ticks = d.pop("IntervalTicks", UNSET)

        _system_event = d.pop("SystemEvent", UNSET)
        system_event: Union[Unset, TasksSystemEvent]
        if isinstance(_system_event, Unset):
            system_event = UNSET
        else:
            system_event = TasksSystemEvent(_system_event)

        _day_of_week = d.pop("DayOfWeek", UNSET)
        day_of_week: Union[Unset, DayOfWeek]
        if isinstance(_day_of_week, Unset):
            day_of_week = UNSET
        else:
            day_of_week = DayOfWeek(_day_of_week)

        max_runtime_ticks = d.pop("MaxRuntimeTicks", UNSET)

        tasks_task_trigger_info = cls(
            type=type,
            time_of_day_ticks=time_of_day_ticks,
            interval_ticks=interval_ticks,
            system_event=system_event,
            day_of_week=day_of_week,
            max_runtime_ticks=max_runtime_ticks,
        )

        tasks_task_trigger_info.additional_properties = d
        return tasks_task_trigger_info

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
