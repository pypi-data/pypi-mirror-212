from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.time_span import TimeSpan


T = TypeVar("T", bound="ProcessRunMetricsProcessMetricPoint")


@attr.s(auto_attribs=True)
class ProcessRunMetricsProcessMetricPoint:
    """
    Attributes:
        time (Union[Unset, TimeSpan]):
        cpu_percent (Union[Unset, float]):
        virtual_memory (Union[Unset, float]):
        working_set (Union[Unset, float]):
    """

    time: Union[Unset, "TimeSpan"] = UNSET
    cpu_percent: Union[Unset, float] = UNSET
    virtual_memory: Union[Unset, float] = UNSET
    working_set: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        time: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.time, Unset):
            time = self.time.to_dict()

        cpu_percent = self.cpu_percent
        virtual_memory = self.virtual_memory
        working_set = self.working_set

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if time is not UNSET:
            field_dict["Time"] = time
        if cpu_percent is not UNSET:
            field_dict["CpuPercent"] = cpu_percent
        if virtual_memory is not UNSET:
            field_dict["VirtualMemory"] = virtual_memory
        if working_set is not UNSET:
            field_dict["WorkingSet"] = working_set

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.time_span import TimeSpan

        d = src_dict.copy()
        _time = d.pop("Time", UNSET)
        time: Union[Unset, TimeSpan]
        if isinstance(_time, Unset):
            time = UNSET
        else:
            time = TimeSpan.from_dict(_time)

        cpu_percent = d.pop("CpuPercent", UNSET)

        virtual_memory = d.pop("VirtualMemory", UNSET)

        working_set = d.pop("WorkingSet", UNSET)

        process_run_metrics_process_metric_point = cls(
            time=time,
            cpu_percent=cpu_percent,
            virtual_memory=virtual_memory,
            working_set=working_set,
        )

        process_run_metrics_process_metric_point.additional_properties = d
        return process_run_metrics_process_metric_point

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
