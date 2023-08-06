from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PublicSystemInfo")


@attr.s(auto_attribs=True)
class PublicSystemInfo:
    """
    Attributes:
        local_address (Union[Unset, str]):
        local_addresses (Union[Unset, List[str]]):
        wan_address (Union[Unset, str]):
        remote_addresses (Union[Unset, List[str]]):
        server_name (Union[Unset, str]):
        version (Union[Unset, str]):
        id (Union[Unset, str]):
    """

    local_address: Union[Unset, str] = UNSET
    local_addresses: Union[Unset, List[str]] = UNSET
    wan_address: Union[Unset, str] = UNSET
    remote_addresses: Union[Unset, List[str]] = UNSET
    server_name: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        local_address = self.local_address
        local_addresses: Union[Unset, List[str]] = UNSET
        if not isinstance(self.local_addresses, Unset):
            local_addresses = self.local_addresses

        wan_address = self.wan_address
        remote_addresses: Union[Unset, List[str]] = UNSET
        if not isinstance(self.remote_addresses, Unset):
            remote_addresses = self.remote_addresses

        server_name = self.server_name
        version = self.version
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if local_address is not UNSET:
            field_dict["LocalAddress"] = local_address
        if local_addresses is not UNSET:
            field_dict["LocalAddresses"] = local_addresses
        if wan_address is not UNSET:
            field_dict["WanAddress"] = wan_address
        if remote_addresses is not UNSET:
            field_dict["RemoteAddresses"] = remote_addresses
        if server_name is not UNSET:
            field_dict["ServerName"] = server_name
        if version is not UNSET:
            field_dict["Version"] = version
        if id is not UNSET:
            field_dict["Id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        local_address = d.pop("LocalAddress", UNSET)

        local_addresses = cast(List[str], d.pop("LocalAddresses", UNSET))

        wan_address = d.pop("WanAddress", UNSET)

        remote_addresses = cast(List[str], d.pop("RemoteAddresses", UNSET))

        server_name = d.pop("ServerName", UNSET)

        version = d.pop("Version", UNSET)

        id = d.pop("Id", UNSET)

        public_system_info = cls(
            local_address=local_address,
            local_addresses=local_addresses,
            wan_address=wan_address,
            remote_addresses=remote_addresses,
            server_name=server_name,
            version=version,
            id=id,
        )

        public_system_info.additional_properties = d
        return public_system_info

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
