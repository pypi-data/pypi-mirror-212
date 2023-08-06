from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmbyNotificationsNotificationTypeInfo")


@attr.s(auto_attribs=True)
class EmbyNotificationsNotificationTypeInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        id (Union[Unset, str]):
        category_name (Union[Unset, str]):
        category_id (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    category_name: Union[Unset, str] = UNSET
    category_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        category_name = self.category_name
        category_id = self.category_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if id is not UNSET:
            field_dict["Id"] = id
        if category_name is not UNSET:
            field_dict["CategoryName"] = category_name
        if category_id is not UNSET:
            field_dict["CategoryId"] = category_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        id = d.pop("Id", UNSET)

        category_name = d.pop("CategoryName", UNSET)

        category_id = d.pop("CategoryId", UNSET)

        emby_notifications_notification_type_info = cls(
            name=name,
            id=id,
            category_name=category_name,
            category_id=category_id,
        )

        emby_notifications_notification_type_info.additional_properties = d
        return emby_notifications_notification_type_info

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
