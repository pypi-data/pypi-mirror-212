from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DevicesLocalFileInfo")


@attr.s(auto_attribs=True)
class DevicesLocalFileInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        id (Union[Unset, str]):
        album (Union[Unset, str]):
        mime_type (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    album: Union[Unset, str] = UNSET
    mime_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        album = self.album
        mime_type = self.mime_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if id is not UNSET:
            field_dict["Id"] = id
        if album is not UNSET:
            field_dict["Album"] = album
        if mime_type is not UNSET:
            field_dict["MimeType"] = mime_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        id = d.pop("Id", UNSET)

        album = d.pop("Album", UNSET)

        mime_type = d.pop("MimeType", UNSET)

        devices_local_file_info = cls(
            name=name,
            id=id,
            album=album,
            mime_type=mime_type,
        )

        devices_local_file_info.additional_properties = d
        return devices_local_file_info

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
