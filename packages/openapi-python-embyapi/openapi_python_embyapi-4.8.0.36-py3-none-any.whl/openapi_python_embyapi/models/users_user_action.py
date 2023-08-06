import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.users_user_action_type import UsersUserActionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="UsersUserAction")


@attr.s(auto_attribs=True)
class UsersUserAction:
    """
    Attributes:
        id (Union[Unset, str]):
        server_id (Union[Unset, str]):
        user_id (Union[Unset, str]):
        item_id (Union[Unset, str]):
        type (Union[Unset, UsersUserActionType]):
        date (Union[Unset, datetime.datetime]):
        position_ticks (Union[Unset, None, int]):
    """

    id: Union[Unset, str] = UNSET
    server_id: Union[Unset, str] = UNSET
    user_id: Union[Unset, str] = UNSET
    item_id: Union[Unset, str] = UNSET
    type: Union[Unset, UsersUserActionType] = UNSET
    date: Union[Unset, datetime.datetime] = UNSET
    position_ticks: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        server_id = self.server_id
        user_id = self.user_id
        item_id = self.item_id
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        position_ticks = self.position_ticks

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if server_id is not UNSET:
            field_dict["ServerId"] = server_id
        if user_id is not UNSET:
            field_dict["UserId"] = user_id
        if item_id is not UNSET:
            field_dict["ItemId"] = item_id
        if type is not UNSET:
            field_dict["Type"] = type
        if date is not UNSET:
            field_dict["Date"] = date
        if position_ticks is not UNSET:
            field_dict["PositionTicks"] = position_ticks

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        server_id = d.pop("ServerId", UNSET)

        user_id = d.pop("UserId", UNSET)

        item_id = d.pop("ItemId", UNSET)

        _type = d.pop("Type", UNSET)
        type: Union[Unset, UsersUserActionType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = UsersUserActionType(_type)

        _date = d.pop("Date", UNSET)
        date: Union[Unset, datetime.datetime]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date)

        position_ticks = d.pop("PositionTicks", UNSET)

        users_user_action = cls(
            id=id,
            server_id=server_id,
            user_id=user_id,
            item_id=item_id,
            type=type,
            date=date,
            position_ticks=position_ticks,
        )

        users_user_action.additional_properties = d
        return users_user_action

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
