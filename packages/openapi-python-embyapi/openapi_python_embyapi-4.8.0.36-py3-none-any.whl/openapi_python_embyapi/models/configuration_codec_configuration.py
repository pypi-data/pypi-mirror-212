from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConfigurationCodecConfiguration")


@attr.s(auto_attribs=True)
class ConfigurationCodecConfiguration:
    """
    Attributes:
        is_enabled (Union[Unset, bool]):
        priority (Union[Unset, int]):
        codec_id (Union[Unset, str]):
    """

    is_enabled: Union[Unset, bool] = UNSET
    priority: Union[Unset, int] = UNSET
    codec_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_enabled = self.is_enabled
        priority = self.priority
        codec_id = self.codec_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_enabled is not UNSET:
            field_dict["IsEnabled"] = is_enabled
        if priority is not UNSET:
            field_dict["Priority"] = priority
        if codec_id is not UNSET:
            field_dict["CodecId"] = codec_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_enabled = d.pop("IsEnabled", UNSET)

        priority = d.pop("Priority", UNSET)

        codec_id = d.pop("CodecId", UNSET)

        configuration_codec_configuration = cls(
            is_enabled=is_enabled,
            priority=priority,
            codec_id=codec_id,
        )

        configuration_codec_configuration.additional_properties = d
        return configuration_codec_configuration

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
