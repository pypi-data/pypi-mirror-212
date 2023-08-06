from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmbyWebGenericUIApiEndpointsRunUICommand")


@attr.s(auto_attribs=True)
class EmbyWebGenericUIApiEndpointsRunUICommand:
    """
    Attributes:
        page_id (Union[Unset, str]):
        command_id (Union[Unset, str]):
        data (Union[Unset, str]):
        item_id (Union[Unset, str]):
        client_locale (Union[Unset, str]):
    """

    page_id: Union[Unset, str] = UNSET
    command_id: Union[Unset, str] = UNSET
    data: Union[Unset, str] = UNSET
    item_id: Union[Unset, str] = UNSET
    client_locale: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        page_id = self.page_id
        command_id = self.command_id
        data = self.data
        item_id = self.item_id
        client_locale = self.client_locale

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if page_id is not UNSET:
            field_dict["PageId"] = page_id
        if command_id is not UNSET:
            field_dict["CommandId"] = command_id
        if data is not UNSET:
            field_dict["Data"] = data
        if item_id is not UNSET:
            field_dict["ItemId"] = item_id
        if client_locale is not UNSET:
            field_dict["ClientLocale"] = client_locale

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        page_id = d.pop("PageId", UNSET)

        command_id = d.pop("CommandId", UNSET)

        data = d.pop("Data", UNSET)

        item_id = d.pop("ItemId", UNSET)

        client_locale = d.pop("ClientLocale", UNSET)

        emby_web_generic_ui_api_endpoints_run_ui_command = cls(
            page_id=page_id,
            command_id=command_id,
            data=data,
            item_id=item_id,
            client_locale=client_locale,
        )

        emby_web_generic_ui_api_endpoints_run_ui_command.additional_properties = d
        return emby_web_generic_ui_api_endpoints_run_ui_command

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
