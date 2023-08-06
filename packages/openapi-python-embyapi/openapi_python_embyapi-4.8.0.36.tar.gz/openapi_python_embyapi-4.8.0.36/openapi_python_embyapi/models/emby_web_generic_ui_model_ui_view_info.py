from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.emby_web_generic_ui_model_enums_ui_view_type import EmbyWebGenericUIModelEnumsUIViewType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.emby_web_generic_ui_model_ui_command import EmbyWebGenericUIModelUICommand
    from ..models.emby_web_generic_ui_model_ui_tab_page_info import EmbyWebGenericUIModelUITabPageInfo
    from ..models.generic_edit_i_edit_object_container import GenericEditIEditObjectContainer


T = TypeVar("T", bound="EmbyWebGenericUIModelUIViewInfo")


@attr.s(auto_attribs=True)
class EmbyWebGenericUIModelUIViewInfo:
    """
    Attributes:
        view_id (Union[Unset, str]):
        page_id (Union[Unset, str]):
        caption (Union[Unset, str]):
        sub_caption (Union[Unset, str]):
        plugin_id (Union[Unset, str]):
        view_type (Union[Unset, EmbyWebGenericUIModelEnumsUIViewType]):
        show_dialog_full_screen (Union[Unset, bool]):
        is_in_sequence (Union[Unset, bool]):
        redirect_view_url (Union[Unset, str]):
        edit_object_container (Union[Unset, GenericEditIEditObjectContainer]):
        commands (Union[Unset, List['EmbyWebGenericUIModelUICommand']]):
        tab_page_infos (Union[Unset, List['EmbyWebGenericUIModelUITabPageInfo']]):
        is_page_change_info (Union[Unset, bool]):
    """

    view_id: Union[Unset, str] = UNSET
    page_id: Union[Unset, str] = UNSET
    caption: Union[Unset, str] = UNSET
    sub_caption: Union[Unset, str] = UNSET
    plugin_id: Union[Unset, str] = UNSET
    view_type: Union[Unset, EmbyWebGenericUIModelEnumsUIViewType] = UNSET
    show_dialog_full_screen: Union[Unset, bool] = UNSET
    is_in_sequence: Union[Unset, bool] = UNSET
    redirect_view_url: Union[Unset, str] = UNSET
    edit_object_container: Union[Unset, "GenericEditIEditObjectContainer"] = UNSET
    commands: Union[Unset, List["EmbyWebGenericUIModelUICommand"]] = UNSET
    tab_page_infos: Union[Unset, List["EmbyWebGenericUIModelUITabPageInfo"]] = UNSET
    is_page_change_info: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        view_id = self.view_id
        page_id = self.page_id
        caption = self.caption
        sub_caption = self.sub_caption
        plugin_id = self.plugin_id
        view_type: Union[Unset, str] = UNSET
        if not isinstance(self.view_type, Unset):
            view_type = self.view_type.value

        show_dialog_full_screen = self.show_dialog_full_screen
        is_in_sequence = self.is_in_sequence
        redirect_view_url = self.redirect_view_url
        edit_object_container: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.edit_object_container, Unset):
            edit_object_container = self.edit_object_container.to_dict()

        commands: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.commands, Unset):
            commands = []
            for commands_item_data in self.commands:
                commands_item = commands_item_data.to_dict()

                commands.append(commands_item)

        tab_page_infos: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tab_page_infos, Unset):
            tab_page_infos = []
            for tab_page_infos_item_data in self.tab_page_infos:
                tab_page_infos_item = tab_page_infos_item_data.to_dict()

                tab_page_infos.append(tab_page_infos_item)

        is_page_change_info = self.is_page_change_info

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if view_id is not UNSET:
            field_dict["ViewId"] = view_id
        if page_id is not UNSET:
            field_dict["PageId"] = page_id
        if caption is not UNSET:
            field_dict["Caption"] = caption
        if sub_caption is not UNSET:
            field_dict["SubCaption"] = sub_caption
        if plugin_id is not UNSET:
            field_dict["PluginId"] = plugin_id
        if view_type is not UNSET:
            field_dict["ViewType"] = view_type
        if show_dialog_full_screen is not UNSET:
            field_dict["ShowDialogFullScreen"] = show_dialog_full_screen
        if is_in_sequence is not UNSET:
            field_dict["IsInSequence"] = is_in_sequence
        if redirect_view_url is not UNSET:
            field_dict["RedirectViewUrl"] = redirect_view_url
        if edit_object_container is not UNSET:
            field_dict["EditObjectContainer"] = edit_object_container
        if commands is not UNSET:
            field_dict["Commands"] = commands
        if tab_page_infos is not UNSET:
            field_dict["TabPageInfos"] = tab_page_infos
        if is_page_change_info is not UNSET:
            field_dict["IsPageChangeInfo"] = is_page_change_info

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.emby_web_generic_ui_model_ui_command import EmbyWebGenericUIModelUICommand
        from ..models.emby_web_generic_ui_model_ui_tab_page_info import EmbyWebGenericUIModelUITabPageInfo
        from ..models.generic_edit_i_edit_object_container import GenericEditIEditObjectContainer

        d = src_dict.copy()
        view_id = d.pop("ViewId", UNSET)

        page_id = d.pop("PageId", UNSET)

        caption = d.pop("Caption", UNSET)

        sub_caption = d.pop("SubCaption", UNSET)

        plugin_id = d.pop("PluginId", UNSET)

        _view_type = d.pop("ViewType", UNSET)
        view_type: Union[Unset, EmbyWebGenericUIModelEnumsUIViewType]
        if isinstance(_view_type, Unset):
            view_type = UNSET
        else:
            view_type = EmbyWebGenericUIModelEnumsUIViewType(_view_type)

        show_dialog_full_screen = d.pop("ShowDialogFullScreen", UNSET)

        is_in_sequence = d.pop("IsInSequence", UNSET)

        redirect_view_url = d.pop("RedirectViewUrl", UNSET)

        _edit_object_container = d.pop("EditObjectContainer", UNSET)
        edit_object_container: Union[Unset, GenericEditIEditObjectContainer]
        if isinstance(_edit_object_container, Unset):
            edit_object_container = UNSET
        else:
            edit_object_container = GenericEditIEditObjectContainer.from_dict(_edit_object_container)

        commands = []
        _commands = d.pop("Commands", UNSET)
        for commands_item_data in _commands or []:
            commands_item = EmbyWebGenericUIModelUICommand.from_dict(commands_item_data)

            commands.append(commands_item)

        tab_page_infos = []
        _tab_page_infos = d.pop("TabPageInfos", UNSET)
        for tab_page_infos_item_data in _tab_page_infos or []:
            tab_page_infos_item = EmbyWebGenericUIModelUITabPageInfo.from_dict(tab_page_infos_item_data)

            tab_page_infos.append(tab_page_infos_item)

        is_page_change_info = d.pop("IsPageChangeInfo", UNSET)

        emby_web_generic_ui_model_ui_view_info = cls(
            view_id=view_id,
            page_id=page_id,
            caption=caption,
            sub_caption=sub_caption,
            plugin_id=plugin_id,
            view_type=view_type,
            show_dialog_full_screen=show_dialog_full_screen,
            is_in_sequence=is_in_sequence,
            redirect_view_url=redirect_view_url,
            edit_object_container=edit_object_container,
            commands=commands,
            tab_page_infos=tab_page_infos,
            is_page_change_info=is_page_change_info,
        )

        emby_web_generic_ui_model_ui_view_info.additional_properties = d
        return emby_web_generic_ui_model_ui_view_info

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
