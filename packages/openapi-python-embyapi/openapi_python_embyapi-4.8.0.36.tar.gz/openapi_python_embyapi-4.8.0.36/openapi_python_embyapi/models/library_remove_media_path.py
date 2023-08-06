from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LibraryRemoveMediaPath")


@attr.s(auto_attribs=True)
class LibraryRemoveMediaPath:
    """
    Attributes:
        id (Union[Unset, str]):
        path (Union[Unset, str]):
        refresh_library (Union[Unset, bool]):
    """

    id: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    refresh_library: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        path = self.path
        refresh_library = self.refresh_library

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if path is not UNSET:
            field_dict["Path"] = path
        if refresh_library is not UNSET:
            field_dict["RefreshLibrary"] = refresh_library

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        path = d.pop("Path", UNSET)

        refresh_library = d.pop("RefreshLibrary", UNSET)

        library_remove_media_path = cls(
            id=id,
            path=path,
            refresh_library=refresh_library,
        )

        library_remove_media_path.additional_properties = d
        return library_remove_media_path

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
