from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NetEndPointInfo")


@attr.s(auto_attribs=True)
class NetEndPointInfo:
    """
    Attributes:
        is_local (Union[Unset, bool]):
        is_in_network (Union[Unset, bool]):
    """

    is_local: Union[Unset, bool] = UNSET
    is_in_network: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_local = self.is_local
        is_in_network = self.is_in_network

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_local is not UNSET:
            field_dict["IsLocal"] = is_local
        if is_in_network is not UNSET:
            field_dict["IsInNetwork"] = is_in_network

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_local = d.pop("IsLocal", UNSET)

        is_in_network = d.pop("IsInNetwork", UNSET)

        net_end_point_info = cls(
            is_local=is_local,
            is_in_network=is_in_network,
        )

        net_end_point_info.additional_properties = d
        return net_end_point_info

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
