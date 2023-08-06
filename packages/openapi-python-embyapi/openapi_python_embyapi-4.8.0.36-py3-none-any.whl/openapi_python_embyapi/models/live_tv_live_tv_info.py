from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LiveTvLiveTvInfo")


@attr.s(auto_attribs=True)
class LiveTvLiveTvInfo:
    """
    Attributes:
        is_enabled (Union[Unset, bool]):
        enabled_users (Union[Unset, List[str]]):
    """

    is_enabled: Union[Unset, bool] = UNSET
    enabled_users: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_enabled = self.is_enabled
        enabled_users: Union[Unset, List[str]] = UNSET
        if not isinstance(self.enabled_users, Unset):
            enabled_users = self.enabled_users

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_enabled is not UNSET:
            field_dict["IsEnabled"] = is_enabled
        if enabled_users is not UNSET:
            field_dict["EnabledUsers"] = enabled_users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_enabled = d.pop("IsEnabled", UNSET)

        enabled_users = cast(List[str], d.pop("EnabledUsers", UNSET))

        live_tv_live_tv_info = cls(
            is_enabled=is_enabled,
            enabled_users=enabled_users,
        )

        live_tv_live_tv_info.additional_properties = d
        return live_tv_live_tv_info

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
