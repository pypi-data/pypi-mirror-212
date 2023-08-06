from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LiveTVApiSetChannelMapping")


@attr.s(auto_attribs=True)
class LiveTVApiSetChannelMapping:
    """
    Attributes:
        tuner_channel_id (Union[Unset, str]):
        provider_channel_id (Union[Unset, str]):
    """

    tuner_channel_id: Union[Unset, str] = UNSET
    provider_channel_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tuner_channel_id = self.tuner_channel_id
        provider_channel_id = self.provider_channel_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tuner_channel_id is not UNSET:
            field_dict["TunerChannelId"] = tuner_channel_id
        if provider_channel_id is not UNSET:
            field_dict["ProviderChannelId"] = provider_channel_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tuner_channel_id = d.pop("TunerChannelId", UNSET)

        provider_channel_id = d.pop("ProviderChannelId", UNSET)

        live_tv_api_set_channel_mapping = cls(
            tuner_channel_id=tuner_channel_id,
            provider_channel_id=provider_channel_id,
        )

        live_tv_api_set_channel_mapping.additional_properties = d
        return live_tv_api_set_channel_mapping

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
