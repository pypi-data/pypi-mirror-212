from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SessionUserInfo")


@attr.s(auto_attribs=True)
class SessionUserInfo:
    """
    Attributes:
        user_id (Union[Unset, str]):
        user_name (Union[Unset, str]):
        user_internal_id (Union[Unset, int]):
    """

    user_id: Union[Unset, str] = UNSET
    user_name: Union[Unset, str] = UNSET
    user_internal_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        user_name = self.user_name
        user_internal_id = self.user_internal_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user_id is not UNSET:
            field_dict["UserId"] = user_id
        if user_name is not UNSET:
            field_dict["UserName"] = user_name
        if user_internal_id is not UNSET:
            field_dict["UserInternalId"] = user_internal_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("UserId", UNSET)

        user_name = d.pop("UserName", UNSET)

        user_internal_id = d.pop("UserInternalId", UNSET)

        session_user_info = cls(
            user_id=user_id,
            user_name=user_name,
            user_internal_id=user_internal_id,
        )

        session_user_info.additional_properties = d
        return session_user_info

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
