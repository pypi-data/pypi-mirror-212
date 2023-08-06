from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LibraryMediaUpdateInfo")


@attr.s(auto_attribs=True)
class LibraryMediaUpdateInfo:
    """
    Attributes:
        path (Union[Unset, str]):
        update_type (Union[Unset, str]):
    """

    path: Union[Unset, str] = UNSET
    update_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        update_type = self.update_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["Path"] = path
        if update_type is not UNSET:
            field_dict["UpdateType"] = update_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("Path", UNSET)

        update_type = d.pop("UpdateType", UNSET)

        library_media_update_info = cls(
            path=path,
            update_type=update_type,
        )

        library_media_update_info.additional_properties = d
        return library_media_update_info

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
