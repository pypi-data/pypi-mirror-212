from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.io_file_system_entry_type import IOFileSystemEntryType
from ..types import UNSET, Unset

T = TypeVar("T", bound="IOFileSystemEntryInfo")


@attr.s(auto_attribs=True)
class IOFileSystemEntryInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        path (Union[Unset, str]):
        type (Union[Unset, IOFileSystemEntryType]):
    """

    name: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    type: Union[Unset, IOFileSystemEntryType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        path = self.path
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if path is not UNSET:
            field_dict["Path"] = path
        if type is not UNSET:
            field_dict["Type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        path = d.pop("Path", UNSET)

        _type = d.pop("Type", UNSET)
        type: Union[Unset, IOFileSystemEntryType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = IOFileSystemEntryType(_type)

        io_file_system_entry_info = cls(
            name=name,
            path=path,
            type=type,
        )

        io_file_system_entry_info.additional_properties = d
        return io_file_system_entry_info

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
