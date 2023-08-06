from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LiveTVApiSetChannelDisabled")


@attr.s(auto_attribs=True)
class LiveTVApiSetChannelDisabled:
    """
    Attributes:
        id (Union[Unset, str]):
        management_id (Union[Unset, str]):
        disabled (Union[Unset, bool]):
    """

    id: Union[Unset, str] = UNSET
    management_id: Union[Unset, str] = UNSET
    disabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        management_id = self.management_id
        disabled = self.disabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if management_id is not UNSET:
            field_dict["ManagementId"] = management_id
        if disabled is not UNSET:
            field_dict["Disabled"] = disabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        management_id = d.pop("ManagementId", UNSET)

        disabled = d.pop("Disabled", UNSET)

        live_tv_api_set_channel_disabled = cls(
            id=id,
            management_id=management_id,
            disabled=disabled,
        )

        live_tv_api_set_channel_disabled.additional_properties = d
        return live_tv_api_set_channel_disabled

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
