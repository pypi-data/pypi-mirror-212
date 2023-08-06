from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="WakeOnLanInfo")


@attr.s(auto_attribs=True)
class WakeOnLanInfo:
    """
    Attributes:
        mac_address (Union[Unset, str]):
        broadcast_address (Union[Unset, str]):
        port (Union[Unset, int]):
    """

    mac_address: Union[Unset, str] = UNSET
    broadcast_address: Union[Unset, str] = UNSET
    port: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mac_address = self.mac_address
        broadcast_address = self.broadcast_address
        port = self.port

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mac_address is not UNSET:
            field_dict["MacAddress"] = mac_address
        if broadcast_address is not UNSET:
            field_dict["BroadcastAddress"] = broadcast_address
        if port is not UNSET:
            field_dict["Port"] = port

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        mac_address = d.pop("MacAddress", UNSET)

        broadcast_address = d.pop("BroadcastAddress", UNSET)

        port = d.pop("Port", UNSET)

        wake_on_lan_info = cls(
            mac_address=mac_address,
            broadcast_address=broadcast_address,
            port=port,
        )

        wake_on_lan_info.additional_properties = d
        return wake_on_lan_info

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
