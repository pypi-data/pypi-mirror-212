from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.plugins_configuration_page_type import PluginsConfigurationPageType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.common_plugins_i_plugin import CommonPluginsIPlugin


T = TypeVar("T", bound="EmbyWebApiConfigurationPageInfo")


@attr.s(auto_attribs=True)
class EmbyWebApiConfigurationPageInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        enable_in_main_menu (Union[Unset, bool]):
        enable_in_user_menu (Union[Unset, bool]):
        feature_id (Union[Unset, str]):
        menu_section (Union[Unset, str]):
        menu_icon (Union[Unset, str]):
        display_name (Union[Unset, str]):
        configuration_page_type (Union[Unset, PluginsConfigurationPageType]):
        plugin_id (Union[Unset, str]):
        href (Union[Unset, str]):
        nav_menu_id (Union[Unset, str]):
        plugin (Union[Unset, CommonPluginsIPlugin]):
        translations (Union[Unset, List[str]]):
    """

    name: Union[Unset, str] = UNSET
    enable_in_main_menu: Union[Unset, bool] = UNSET
    enable_in_user_menu: Union[Unset, bool] = UNSET
    feature_id: Union[Unset, str] = UNSET
    menu_section: Union[Unset, str] = UNSET
    menu_icon: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    configuration_page_type: Union[Unset, PluginsConfigurationPageType] = UNSET
    plugin_id: Union[Unset, str] = UNSET
    href: Union[Unset, str] = UNSET
    nav_menu_id: Union[Unset, str] = UNSET
    plugin: Union[Unset, "CommonPluginsIPlugin"] = UNSET
    translations: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        enable_in_main_menu = self.enable_in_main_menu
        enable_in_user_menu = self.enable_in_user_menu
        feature_id = self.feature_id
        menu_section = self.menu_section
        menu_icon = self.menu_icon
        display_name = self.display_name
        configuration_page_type: Union[Unset, str] = UNSET
        if not isinstance(self.configuration_page_type, Unset):
            configuration_page_type = self.configuration_page_type.value

        plugin_id = self.plugin_id
        href = self.href
        nav_menu_id = self.nav_menu_id
        plugin: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.plugin, Unset):
            plugin = self.plugin.to_dict()

        translations: Union[Unset, List[str]] = UNSET
        if not isinstance(self.translations, Unset):
            translations = self.translations

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if enable_in_main_menu is not UNSET:
            field_dict["EnableInMainMenu"] = enable_in_main_menu
        if enable_in_user_menu is not UNSET:
            field_dict["EnableInUserMenu"] = enable_in_user_menu
        if feature_id is not UNSET:
            field_dict["FeatureId"] = feature_id
        if menu_section is not UNSET:
            field_dict["MenuSection"] = menu_section
        if menu_icon is not UNSET:
            field_dict["MenuIcon"] = menu_icon
        if display_name is not UNSET:
            field_dict["DisplayName"] = display_name
        if configuration_page_type is not UNSET:
            field_dict["ConfigurationPageType"] = configuration_page_type
        if plugin_id is not UNSET:
            field_dict["PluginId"] = plugin_id
        if href is not UNSET:
            field_dict["Href"] = href
        if nav_menu_id is not UNSET:
            field_dict["NavMenuId"] = nav_menu_id
        if plugin is not UNSET:
            field_dict["Plugin"] = plugin
        if translations is not UNSET:
            field_dict["Translations"] = translations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.common_plugins_i_plugin import CommonPluginsIPlugin

        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        enable_in_main_menu = d.pop("EnableInMainMenu", UNSET)

        enable_in_user_menu = d.pop("EnableInUserMenu", UNSET)

        feature_id = d.pop("FeatureId", UNSET)

        menu_section = d.pop("MenuSection", UNSET)

        menu_icon = d.pop("MenuIcon", UNSET)

        display_name = d.pop("DisplayName", UNSET)

        _configuration_page_type = d.pop("ConfigurationPageType", UNSET)
        configuration_page_type: Union[Unset, PluginsConfigurationPageType]
        if isinstance(_configuration_page_type, Unset):
            configuration_page_type = UNSET
        else:
            configuration_page_type = PluginsConfigurationPageType(_configuration_page_type)

        plugin_id = d.pop("PluginId", UNSET)

        href = d.pop("Href", UNSET)

        nav_menu_id = d.pop("NavMenuId", UNSET)

        _plugin = d.pop("Plugin", UNSET)
        plugin: Union[Unset, CommonPluginsIPlugin]
        if isinstance(_plugin, Unset):
            plugin = UNSET
        else:
            plugin = CommonPluginsIPlugin.from_dict(_plugin)

        translations = cast(List[str], d.pop("Translations", UNSET))

        emby_web_api_configuration_page_info = cls(
            name=name,
            enable_in_main_menu=enable_in_main_menu,
            enable_in_user_menu=enable_in_user_menu,
            feature_id=feature_id,
            menu_section=menu_section,
            menu_icon=menu_icon,
            display_name=display_name,
            configuration_page_type=configuration_page_type,
            plugin_id=plugin_id,
            href=href,
            nav_menu_id=nav_menu_id,
            plugin=plugin,
            translations=translations,
        )

        emby_web_api_configuration_page_info.additional_properties = d
        return emby_web_api_configuration_page_info

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
