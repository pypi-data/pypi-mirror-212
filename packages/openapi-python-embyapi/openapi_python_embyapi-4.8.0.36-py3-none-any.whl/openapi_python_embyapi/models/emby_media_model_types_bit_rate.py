from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmbyMediaModelTypesBitRate")


@attr.s(auto_attribs=True)
class EmbyMediaModelTypesBitRate:
    """
    Attributes:
        bps (Union[Unset, int]):
        kbps (Union[Unset, float]):
        mbps (Union[Unset, float]):
    """

    bps: Union[Unset, int] = UNSET
    kbps: Union[Unset, float] = UNSET
    mbps: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bps = self.bps
        kbps = self.kbps
        mbps = self.mbps

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bps is not UNSET:
            field_dict["bps"] = bps
        if kbps is not UNSET:
            field_dict["kbps"] = kbps
        if mbps is not UNSET:
            field_dict["Mbps"] = mbps

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bps = d.pop("bps", UNSET)

        kbps = d.pop("kbps", UNSET)

        mbps = d.pop("Mbps", UNSET)

        emby_media_model_types_bit_rate = cls(
            bps=bps,
            kbps=kbps,
            mbps=mbps,
        )

        emby_media_model_types_bit_rate.additional_properties = d
        return emby_media_model_types_bit_rate

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
