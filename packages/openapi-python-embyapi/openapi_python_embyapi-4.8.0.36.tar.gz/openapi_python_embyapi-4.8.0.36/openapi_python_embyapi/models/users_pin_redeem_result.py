from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UsersPinRedeemResult")


@attr.s(auto_attribs=True)
class UsersPinRedeemResult:
    """
    Attributes:
        success (Union[Unset, bool]):
        users_reset (Union[Unset, List[str]]):
    """

    success: Union[Unset, bool] = UNSET
    users_reset: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        success = self.success
        users_reset: Union[Unset, List[str]] = UNSET
        if not isinstance(self.users_reset, Unset):
            users_reset = self.users_reset

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if success is not UNSET:
            field_dict["Success"] = success
        if users_reset is not UNSET:
            field_dict["UsersReset"] = users_reset

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        success = d.pop("Success", UNSET)

        users_reset = cast(List[str], d.pop("UsersReset", UNSET))

        users_pin_redeem_result = cls(
            success=success,
            users_reset=users_reset,
        )

        users_pin_redeem_result.additional_properties = d
        return users_pin_redeem_result

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
