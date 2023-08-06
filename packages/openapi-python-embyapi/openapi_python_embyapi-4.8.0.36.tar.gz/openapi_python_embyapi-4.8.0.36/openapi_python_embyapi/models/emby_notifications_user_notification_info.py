from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.emby_notifications_user_notification_info_options import EmbyNotificationsUserNotificationInfoOptions


T = TypeVar("T", bound="EmbyNotificationsUserNotificationInfo")


@attr.s(auto_attribs=True)
class EmbyNotificationsUserNotificationInfo:
    """
    Attributes:
        notifier_key (Union[Unset, str]):
        setup_module_url (Union[Unset, str]):
        service_name (Union[Unset, str]):
        friendly_name (Union[Unset, str]):
        id (Union[Unset, str]):
        enabled (Union[Unset, bool]):
        user_ids (Union[Unset, List[str]]):
        library_ids (Union[Unset, List[str]]):
        event_ids (Union[Unset, List[str]]):
        user_id (Union[Unset, str]):
        is_self_notification (Union[Unset, bool]):
        options (Union[Unset, EmbyNotificationsUserNotificationInfoOptions]):
    """

    notifier_key: Union[Unset, str] = UNSET
    setup_module_url: Union[Unset, str] = UNSET
    service_name: Union[Unset, str] = UNSET
    friendly_name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    user_ids: Union[Unset, List[str]] = UNSET
    library_ids: Union[Unset, List[str]] = UNSET
    event_ids: Union[Unset, List[str]] = UNSET
    user_id: Union[Unset, str] = UNSET
    is_self_notification: Union[Unset, bool] = UNSET
    options: Union[Unset, "EmbyNotificationsUserNotificationInfoOptions"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        notifier_key = self.notifier_key
        setup_module_url = self.setup_module_url
        service_name = self.service_name
        friendly_name = self.friendly_name
        id = self.id
        enabled = self.enabled
        user_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.user_ids, Unset):
            user_ids = self.user_ids

        library_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.library_ids, Unset):
            library_ids = self.library_ids

        event_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.event_ids, Unset):
            event_ids = self.event_ids

        user_id = self.user_id
        is_self_notification = self.is_self_notification
        options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if notifier_key is not UNSET:
            field_dict["NotifierKey"] = notifier_key
        if setup_module_url is not UNSET:
            field_dict["SetupModuleUrl"] = setup_module_url
        if service_name is not UNSET:
            field_dict["ServiceName"] = service_name
        if friendly_name is not UNSET:
            field_dict["FriendlyName"] = friendly_name
        if id is not UNSET:
            field_dict["Id"] = id
        if enabled is not UNSET:
            field_dict["Enabled"] = enabled
        if user_ids is not UNSET:
            field_dict["UserIds"] = user_ids
        if library_ids is not UNSET:
            field_dict["LibraryIds"] = library_ids
        if event_ids is not UNSET:
            field_dict["EventIds"] = event_ids
        if user_id is not UNSET:
            field_dict["UserId"] = user_id
        if is_self_notification is not UNSET:
            field_dict["IsSelfNotification"] = is_self_notification
        if options is not UNSET:
            field_dict["Options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.emby_notifications_user_notification_info_options import (
            EmbyNotificationsUserNotificationInfoOptions,
        )

        d = src_dict.copy()
        notifier_key = d.pop("NotifierKey", UNSET)

        setup_module_url = d.pop("SetupModuleUrl", UNSET)

        service_name = d.pop("ServiceName", UNSET)

        friendly_name = d.pop("FriendlyName", UNSET)

        id = d.pop("Id", UNSET)

        enabled = d.pop("Enabled", UNSET)

        user_ids = cast(List[str], d.pop("UserIds", UNSET))

        library_ids = cast(List[str], d.pop("LibraryIds", UNSET))

        event_ids = cast(List[str], d.pop("EventIds", UNSET))

        user_id = d.pop("UserId", UNSET)

        is_self_notification = d.pop("IsSelfNotification", UNSET)

        _options = d.pop("Options", UNSET)
        options: Union[Unset, EmbyNotificationsUserNotificationInfoOptions]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = EmbyNotificationsUserNotificationInfoOptions.from_dict(_options)

        emby_notifications_user_notification_info = cls(
            notifier_key=notifier_key,
            setup_module_url=setup_module_url,
            service_name=service_name,
            friendly_name=friendly_name,
            id=id,
            enabled=enabled,
            user_ids=user_ids,
            library_ids=library_ids,
            event_ids=event_ids,
            user_id=user_id,
            is_self_notification=is_self_notification,
            options=options,
        )

        emby_notifications_user_notification_info.additional_properties = d
        return emby_notifications_user_notification_info

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
