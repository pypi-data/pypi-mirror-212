from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LibraryRemoveVirtualFolder")


@attr.s(auto_attribs=True)
class LibraryRemoveVirtualFolder:
    """
    Attributes:
        id (Union[Unset, str]):
        refresh_library (Union[Unset, bool]):
    """

    id: Union[Unset, str] = UNSET
    refresh_library: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        refresh_library = self.refresh_library

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if refresh_library is not UNSET:
            field_dict["RefreshLibrary"] = refresh_library

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        refresh_library = d.pop("RefreshLibrary", UNSET)

        library_remove_virtual_folder = cls(
            id=id,
            refresh_library=refresh_library,
        )

        library_remove_virtual_folder.additional_properties = d
        return library_remove_virtual_folder

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
