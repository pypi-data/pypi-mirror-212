from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConnectUserLinkResult")


@attr.s(auto_attribs=True)
class ConnectUserLinkResult:
    """
    Attributes:
        is_pending (Union[Unset, bool]):
        is_new_user_invitation (Union[Unset, bool]):
        guest_display_name (Union[Unset, str]):
    """

    is_pending: Union[Unset, bool] = UNSET
    is_new_user_invitation: Union[Unset, bool] = UNSET
    guest_display_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_pending = self.is_pending
        is_new_user_invitation = self.is_new_user_invitation
        guest_display_name = self.guest_display_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_pending is not UNSET:
            field_dict["IsPending"] = is_pending
        if is_new_user_invitation is not UNSET:
            field_dict["IsNewUserInvitation"] = is_new_user_invitation
        if guest_display_name is not UNSET:
            field_dict["GuestDisplayName"] = guest_display_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_pending = d.pop("IsPending", UNSET)

        is_new_user_invitation = d.pop("IsNewUserInvitation", UNSET)

        guest_display_name = d.pop("GuestDisplayName", UNSET)

        connect_user_link_result = cls(
            is_pending=is_pending,
            is_new_user_invitation=is_new_user_invitation,
            guest_display_name=guest_display_name,
        )

        connect_user_link_result.additional_properties = d
        return connect_user_link_result

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
