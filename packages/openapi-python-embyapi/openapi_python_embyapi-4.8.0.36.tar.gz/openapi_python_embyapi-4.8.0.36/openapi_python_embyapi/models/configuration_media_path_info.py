from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConfigurationMediaPathInfo")


@attr.s(auto_attribs=True)
class ConfigurationMediaPathInfo:
    """
    Attributes:
        path (Union[Unset, str]):
        network_path (Union[Unset, str]):
        username (Union[Unset, str]):
        password (Union[Unset, str]):
    """

    path: Union[Unset, str] = UNSET
    network_path: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        network_path = self.network_path
        username = self.username
        password = self.password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["Path"] = path
        if network_path is not UNSET:
            field_dict["NetworkPath"] = network_path
        if username is not UNSET:
            field_dict["Username"] = username
        if password is not UNSET:
            field_dict["Password"] = password

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("Path", UNSET)

        network_path = d.pop("NetworkPath", UNSET)

        username = d.pop("Username", UNSET)

        password = d.pop("Password", UNSET)

        configuration_media_path_info = cls(
            path=path,
            network_path=network_path,
            username=username,
            password=password,
        )

        configuration_media_path_info.additional_properties = d
        return configuration_media_path_info

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
