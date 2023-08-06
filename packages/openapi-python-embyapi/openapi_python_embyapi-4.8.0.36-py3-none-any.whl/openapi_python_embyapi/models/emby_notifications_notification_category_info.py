from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.emby_notifications_notification_type_info import EmbyNotificationsNotificationTypeInfo


T = TypeVar("T", bound="EmbyNotificationsNotificationCategoryInfo")


@attr.s(auto_attribs=True)
class EmbyNotificationsNotificationCategoryInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        id (Union[Unset, str]):
        events (Union[Unset, List['EmbyNotificationsNotificationTypeInfo']]):
    """

    name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    events: Union[Unset, List["EmbyNotificationsNotificationTypeInfo"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        events: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.events, Unset):
            events = []
            for events_item_data in self.events:
                events_item = events_item_data.to_dict()

                events.append(events_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if id is not UNSET:
            field_dict["Id"] = id
        if events is not UNSET:
            field_dict["Events"] = events

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.emby_notifications_notification_type_info import EmbyNotificationsNotificationTypeInfo

        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        id = d.pop("Id", UNSET)

        events = []
        _events = d.pop("Events", UNSET)
        for events_item_data in _events or []:
            events_item = EmbyNotificationsNotificationTypeInfo.from_dict(events_item_data)

            events.append(events_item)

        emby_notifications_notification_category_info = cls(
            name=name,
            id=id,
            events=events,
        )

        emby_notifications_notification_category_info.additional_properties = d
        return emby_notifications_notification_category_info

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
