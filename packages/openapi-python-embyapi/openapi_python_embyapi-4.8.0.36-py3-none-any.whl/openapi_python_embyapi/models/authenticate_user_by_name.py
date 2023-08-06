from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuthenticateUserByName")


@attr.s(auto_attribs=True)
class AuthenticateUserByName:
    """
    Attributes:
        username (Union[Unset, str]):
        pw (Union[Unset, str]):
    """

    username: Union[Unset, str] = UNSET
    pw: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username
        pw = self.pw

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["Username"] = username
        if pw is not UNSET:
            field_dict["Pw"] = pw

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("Username", UNSET)

        pw = d.pop("Pw", UNSET)

        authenticate_user_by_name = cls(
            username=username,
            pw=pw,
        )

        authenticate_user_by_name.additional_properties = d
        return authenticate_user_by_name

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
