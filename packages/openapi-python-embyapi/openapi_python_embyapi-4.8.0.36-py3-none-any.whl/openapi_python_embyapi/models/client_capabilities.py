from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dlna_device_profile import DlnaDeviceProfile


T = TypeVar("T", bound="ClientCapabilities")


@attr.s(auto_attribs=True)
class ClientCapabilities:
    """
    Attributes:
        playable_media_types (Union[Unset, List[str]]):
        supported_commands (Union[Unset, List[str]]):
        supports_media_control (Union[Unset, bool]):
        push_token (Union[Unset, str]):
        push_token_type (Union[Unset, str]):
        supports_sync (Union[Unset, bool]):
        device_profile (Union[Unset, DlnaDeviceProfile]):
        icon_url (Union[Unset, str]):
        app_id (Union[Unset, str]):
    """

    playable_media_types: Union[Unset, List[str]] = UNSET
    supported_commands: Union[Unset, List[str]] = UNSET
    supports_media_control: Union[Unset, bool] = UNSET
    push_token: Union[Unset, str] = UNSET
    push_token_type: Union[Unset, str] = UNSET
    supports_sync: Union[Unset, bool] = UNSET
    device_profile: Union[Unset, "DlnaDeviceProfile"] = UNSET
    icon_url: Union[Unset, str] = UNSET
    app_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        playable_media_types: Union[Unset, List[str]] = UNSET
        if not isinstance(self.playable_media_types, Unset):
            playable_media_types = self.playable_media_types

        supported_commands: Union[Unset, List[str]] = UNSET
        if not isinstance(self.supported_commands, Unset):
            supported_commands = self.supported_commands

        supports_media_control = self.supports_media_control
        push_token = self.push_token
        push_token_type = self.push_token_type
        supports_sync = self.supports_sync
        device_profile: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.device_profile, Unset):
            device_profile = self.device_profile.to_dict()

        icon_url = self.icon_url
        app_id = self.app_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if playable_media_types is not UNSET:
            field_dict["PlayableMediaTypes"] = playable_media_types
        if supported_commands is not UNSET:
            field_dict["SupportedCommands"] = supported_commands
        if supports_media_control is not UNSET:
            field_dict["SupportsMediaControl"] = supports_media_control
        if push_token is not UNSET:
            field_dict["PushToken"] = push_token
        if push_token_type is not UNSET:
            field_dict["PushTokenType"] = push_token_type
        if supports_sync is not UNSET:
            field_dict["SupportsSync"] = supports_sync
        if device_profile is not UNSET:
            field_dict["DeviceProfile"] = device_profile
        if icon_url is not UNSET:
            field_dict["IconUrl"] = icon_url
        if app_id is not UNSET:
            field_dict["AppId"] = app_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dlna_device_profile import DlnaDeviceProfile

        d = src_dict.copy()
        playable_media_types = cast(List[str], d.pop("PlayableMediaTypes", UNSET))

        supported_commands = cast(List[str], d.pop("SupportedCommands", UNSET))

        supports_media_control = d.pop("SupportsMediaControl", UNSET)

        push_token = d.pop("PushToken", UNSET)

        push_token_type = d.pop("PushTokenType", UNSET)

        supports_sync = d.pop("SupportsSync", UNSET)

        _device_profile = d.pop("DeviceProfile", UNSET)
        device_profile: Union[Unset, DlnaDeviceProfile]
        if isinstance(_device_profile, Unset):
            device_profile = UNSET
        else:
            device_profile = DlnaDeviceProfile.from_dict(_device_profile)

        icon_url = d.pop("IconUrl", UNSET)

        app_id = d.pop("AppId", UNSET)

        client_capabilities = cls(
            playable_media_types=playable_media_types,
            supported_commands=supported_commands,
            supports_media_control=supports_media_control,
            push_token=push_token,
            push_token_type=push_token_type,
            supports_sync=supports_sync,
            device_profile=device_profile,
            icon_url=icon_url,
            app_id=app_id,
        )

        client_capabilities.additional_properties = d
        return client_capabilities

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
