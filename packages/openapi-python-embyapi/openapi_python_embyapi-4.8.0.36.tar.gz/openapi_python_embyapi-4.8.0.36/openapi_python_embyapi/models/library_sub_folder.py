from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LibrarySubFolder")


@attr.s(auto_attribs=True)
class LibrarySubFolder:
    """
    Attributes:
        name (Union[Unset, str]):
        id (Union[Unset, str]):
        path (Union[Unset, str]):
        is_user_access_configurable (Union[Unset, bool]):
    """

    name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    is_user_access_configurable: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        path = self.path
        is_user_access_configurable = self.is_user_access_configurable

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if id is not UNSET:
            field_dict["Id"] = id
        if path is not UNSET:
            field_dict["Path"] = path
        if is_user_access_configurable is not UNSET:
            field_dict["IsUserAccessConfigurable"] = is_user_access_configurable

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        id = d.pop("Id", UNSET)

        path = d.pop("Path", UNSET)

        is_user_access_configurable = d.pop("IsUserAccessConfigurable", UNSET)

        library_sub_folder = cls(
            name=name,
            id=id,
            path=path,
            is_user_access_configurable=is_user_access_configurable,
        )

        library_sub_folder.additional_properties = d
        return library_sub_folder

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
