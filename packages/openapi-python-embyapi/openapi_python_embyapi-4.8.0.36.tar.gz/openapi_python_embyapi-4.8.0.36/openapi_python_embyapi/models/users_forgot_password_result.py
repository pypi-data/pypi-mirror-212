import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.users_forgot_password_action import UsersForgotPasswordAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="UsersForgotPasswordResult")


@attr.s(auto_attribs=True)
class UsersForgotPasswordResult:
    """
    Attributes:
        action (Union[Unset, UsersForgotPasswordAction]):
        pin_file (Union[Unset, str]):
        pin_expiration_date (Union[Unset, None, datetime.datetime]):
    """

    action: Union[Unset, UsersForgotPasswordAction] = UNSET
    pin_file: Union[Unset, str] = UNSET
    pin_expiration_date: Union[Unset, None, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        action: Union[Unset, str] = UNSET
        if not isinstance(self.action, Unset):
            action = self.action.value

        pin_file = self.pin_file
        pin_expiration_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.pin_expiration_date, Unset):
            pin_expiration_date = self.pin_expiration_date.isoformat() if self.pin_expiration_date else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action is not UNSET:
            field_dict["Action"] = action
        if pin_file is not UNSET:
            field_dict["PinFile"] = pin_file
        if pin_expiration_date is not UNSET:
            field_dict["PinExpirationDate"] = pin_expiration_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _action = d.pop("Action", UNSET)
        action: Union[Unset, UsersForgotPasswordAction]
        if isinstance(_action, Unset):
            action = UNSET
        else:
            action = UsersForgotPasswordAction(_action)

        pin_file = d.pop("PinFile", UNSET)

        _pin_expiration_date = d.pop("PinExpirationDate", UNSET)
        pin_expiration_date: Union[Unset, None, datetime.datetime]
        if _pin_expiration_date is None:
            pin_expiration_date = None
        elif isinstance(_pin_expiration_date, Unset):
            pin_expiration_date = UNSET
        else:
            pin_expiration_date = isoparse(_pin_expiration_date)

        users_forgot_password_result = cls(
            action=action,
            pin_file=pin_file,
            pin_expiration_date=pin_expiration_date,
        )

        users_forgot_password_result.additional_properties = d
        return users_forgot_password_result

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
