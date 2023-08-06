from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.tasks_task_state import TasksTaskState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tasks_task_result import TasksTaskResult
    from ..models.tasks_task_trigger_info import TasksTaskTriggerInfo


T = TypeVar("T", bound="TasksTaskInfo")


@attr.s(auto_attribs=True)
class TasksTaskInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        state (Union[Unset, TasksTaskState]):
        current_progress_percentage (Union[Unset, None, float]):
        id (Union[Unset, str]):
        last_execution_result (Union[Unset, TasksTaskResult]):
        triggers (Union[Unset, List['TasksTaskTriggerInfo']]):
        description (Union[Unset, str]):
        category (Union[Unset, str]):
        is_hidden (Union[Unset, bool]):
        key (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    state: Union[Unset, TasksTaskState] = UNSET
    current_progress_percentage: Union[Unset, None, float] = UNSET
    id: Union[Unset, str] = UNSET
    last_execution_result: Union[Unset, "TasksTaskResult"] = UNSET
    triggers: Union[Unset, List["TasksTaskTriggerInfo"]] = UNSET
    description: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    is_hidden: Union[Unset, bool] = UNSET
    key: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        current_progress_percentage = self.current_progress_percentage
        id = self.id
        last_execution_result: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.last_execution_result, Unset):
            last_execution_result = self.last_execution_result.to_dict()

        triggers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.triggers, Unset):
            triggers = []
            for triggers_item_data in self.triggers:
                triggers_item = triggers_item_data.to_dict()

                triggers.append(triggers_item)

        description = self.description
        category = self.category
        is_hidden = self.is_hidden
        key = self.key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if state is not UNSET:
            field_dict["State"] = state
        if current_progress_percentage is not UNSET:
            field_dict["CurrentProgressPercentage"] = current_progress_percentage
        if id is not UNSET:
            field_dict["Id"] = id
        if last_execution_result is not UNSET:
            field_dict["LastExecutionResult"] = last_execution_result
        if triggers is not UNSET:
            field_dict["Triggers"] = triggers
        if description is not UNSET:
            field_dict["Description"] = description
        if category is not UNSET:
            field_dict["Category"] = category
        if is_hidden is not UNSET:
            field_dict["IsHidden"] = is_hidden
        if key is not UNSET:
            field_dict["Key"] = key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tasks_task_result import TasksTaskResult
        from ..models.tasks_task_trigger_info import TasksTaskTriggerInfo

        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        _state = d.pop("State", UNSET)
        state: Union[Unset, TasksTaskState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = TasksTaskState(_state)

        current_progress_percentage = d.pop("CurrentProgressPercentage", UNSET)

        id = d.pop("Id", UNSET)

        _last_execution_result = d.pop("LastExecutionResult", UNSET)
        last_execution_result: Union[Unset, TasksTaskResult]
        if isinstance(_last_execution_result, Unset):
            last_execution_result = UNSET
        else:
            last_execution_result = TasksTaskResult.from_dict(_last_execution_result)

        triggers = []
        _triggers = d.pop("Triggers", UNSET)
        for triggers_item_data in _triggers or []:
            triggers_item = TasksTaskTriggerInfo.from_dict(triggers_item_data)

            triggers.append(triggers_item)

        description = d.pop("Description", UNSET)

        category = d.pop("Category", UNSET)

        is_hidden = d.pop("IsHidden", UNSET)

        key = d.pop("Key", UNSET)

        tasks_task_info = cls(
            name=name,
            state=state,
            current_progress_percentage=current_progress_percentage,
            id=id,
            last_execution_result=last_execution_result,
            triggers=triggers,
            description=description,
            category=category,
            is_hidden=is_hidden,
            key=key,
        )

        tasks_task_info.additional_properties = d
        return tasks_task_info

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
