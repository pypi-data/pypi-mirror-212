from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateUserEasyPassword")


@attr.s(auto_attribs=True)
class UpdateUserEasyPassword:
    """
    Attributes:
        id (Union[Unset, str]):
        new_pw (Union[Unset, str]):
        reset_password (Union[Unset, bool]):
    """

    id: Union[Unset, str] = UNSET
    new_pw: Union[Unset, str] = UNSET
    reset_password: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        new_pw = self.new_pw
        reset_password = self.reset_password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if new_pw is not UNSET:
            field_dict["NewPw"] = new_pw
        if reset_password is not UNSET:
            field_dict["ResetPassword"] = reset_password

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        new_pw = d.pop("NewPw", UNSET)

        reset_password = d.pop("ResetPassword", UNSET)

        update_user_easy_password = cls(
            id=id,
            new_pw=new_pw,
            reset_password=reset_password,
        )

        update_user_easy_password.additional_properties = d
        return update_user_easy_password

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
