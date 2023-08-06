from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PersistenceIntroDebugInfo")


@attr.s(auto_attribs=True)
class PersistenceIntroDebugInfo:
    """
    Attributes:
        id (Union[Unset, int]):
        path (Union[Unset, str]):
        start (Union[Unset, int]):
        end (Union[Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    path: Union[Unset, str] = UNSET
    start: Union[Unset, int] = UNSET
    end: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        path = self.path
        start = self.start
        end = self.end

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if path is not UNSET:
            field_dict["Path"] = path
        if start is not UNSET:
            field_dict["Start"] = start
        if end is not UNSET:
            field_dict["End"] = end

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        path = d.pop("Path", UNSET)

        start = d.pop("Start", UNSET)

        end = d.pop("End", UNSET)

        persistence_intro_debug_info = cls(
            id=id,
            path=path,
            start=start,
            end=end,
        )

        persistence_intro_debug_info.additional_properties = d
        return persistence_intro_debug_info

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
