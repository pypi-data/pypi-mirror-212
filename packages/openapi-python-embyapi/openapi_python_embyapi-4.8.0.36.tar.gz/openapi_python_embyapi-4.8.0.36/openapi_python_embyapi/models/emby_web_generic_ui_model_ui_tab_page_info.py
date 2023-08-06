from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmbyWebGenericUIModelUITabPageInfo")


@attr.s(auto_attribs=True)
class EmbyWebGenericUIModelUITabPageInfo:
    """
    Attributes:
        page_id (Union[Unset, str]):
        display_name (Union[Unset, str]):
        plugin_id (Union[Unset, str]):
        href (Union[Unset, str]):
        nav_key (Union[Unset, str]):
        index (Union[Unset, int]):
    """

    page_id: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    plugin_id: Union[Unset, str] = UNSET
    href: Union[Unset, str] = UNSET
    nav_key: Union[Unset, str] = UNSET
    index: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        page_id = self.page_id
        display_name = self.display_name
        plugin_id = self.plugin_id
        href = self.href
        nav_key = self.nav_key
        index = self.index

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if page_id is not UNSET:
            field_dict["PageId"] = page_id
        if display_name is not UNSET:
            field_dict["DisplayName"] = display_name
        if plugin_id is not UNSET:
            field_dict["PluginId"] = plugin_id
        if href is not UNSET:
            field_dict["Href"] = href
        if nav_key is not UNSET:
            field_dict["NavKey"] = nav_key
        if index is not UNSET:
            field_dict["Index"] = index

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        page_id = d.pop("PageId", UNSET)

        display_name = d.pop("DisplayName", UNSET)

        plugin_id = d.pop("PluginId", UNSET)

        href = d.pop("Href", UNSET)

        nav_key = d.pop("NavKey", UNSET)

        index = d.pop("Index", UNSET)

        emby_web_generic_ui_model_ui_tab_page_info = cls(
            page_id=page_id,
            display_name=display_name,
            plugin_id=plugin_id,
            href=href,
            nav_key=nav_key,
            index=index,
        )

        emby_web_generic_ui_model_ui_tab_page_info.additional_properties = d
        return emby_web_generic_ui_model_ui_tab_page_info

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
