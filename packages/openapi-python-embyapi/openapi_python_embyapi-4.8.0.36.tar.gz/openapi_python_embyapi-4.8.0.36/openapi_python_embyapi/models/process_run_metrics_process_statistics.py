from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.process_run_metrics_process_metric_point import ProcessRunMetricsProcessMetricPoint


T = TypeVar("T", bound="ProcessRunMetricsProcessStatistics")


@attr.s(auto_attribs=True)
class ProcessRunMetricsProcessStatistics:
    """
    Attributes:
        current_cpu (Union[Unset, float]):
        average_cpu (Union[Unset, float]):
        current_virtual_memory (Union[Unset, float]):
        current_working_set (Union[Unset, float]):
        metrics (Union[Unset, List['ProcessRunMetricsProcessMetricPoint']]):
    """

    current_cpu: Union[Unset, float] = UNSET
    average_cpu: Union[Unset, float] = UNSET
    current_virtual_memory: Union[Unset, float] = UNSET
    current_working_set: Union[Unset, float] = UNSET
    metrics: Union[Unset, List["ProcessRunMetricsProcessMetricPoint"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        current_cpu = self.current_cpu
        average_cpu = self.average_cpu
        current_virtual_memory = self.current_virtual_memory
        current_working_set = self.current_working_set
        metrics: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = []
            for metrics_item_data in self.metrics:
                metrics_item = metrics_item_data.to_dict()

                metrics.append(metrics_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if current_cpu is not UNSET:
            field_dict["CurrentCpu"] = current_cpu
        if average_cpu is not UNSET:
            field_dict["AverageCpu"] = average_cpu
        if current_virtual_memory is not UNSET:
            field_dict["CurrentVirtualMemory"] = current_virtual_memory
        if current_working_set is not UNSET:
            field_dict["CurrentWorkingSet"] = current_working_set
        if metrics is not UNSET:
            field_dict["Metrics"] = metrics

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.process_run_metrics_process_metric_point import ProcessRunMetricsProcessMetricPoint

        d = src_dict.copy()
        current_cpu = d.pop("CurrentCpu", UNSET)

        average_cpu = d.pop("AverageCpu", UNSET)

        current_virtual_memory = d.pop("CurrentVirtualMemory", UNSET)

        current_working_set = d.pop("CurrentWorkingSet", UNSET)

        metrics = []
        _metrics = d.pop("Metrics", UNSET)
        for metrics_item_data in _metrics or []:
            metrics_item = ProcessRunMetricsProcessMetricPoint.from_dict(metrics_item_data)

            metrics.append(metrics_item)

        process_run_metrics_process_statistics = cls(
            current_cpu=current_cpu,
            average_cpu=average_cpu,
            current_virtual_memory=current_virtual_memory,
            current_working_set=current_working_set,
            metrics=metrics,
        )

        process_run_metrics_process_statistics.additional_properties = d
        return process_run_metrics_process_statistics

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
