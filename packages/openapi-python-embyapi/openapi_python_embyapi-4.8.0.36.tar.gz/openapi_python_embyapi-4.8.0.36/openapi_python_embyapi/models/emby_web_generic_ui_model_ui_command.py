from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.emby_web_generic_ui_model_enums_ui_command_type import EmbyWebGenericUIModelEnumsUICommandType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmbyWebGenericUIModelUICommand")


@attr.s(auto_attribs=True)
class EmbyWebGenericUIModelUICommand:
    """
    Attributes:
        command_type (Union[Unset, EmbyWebGenericUIModelEnumsUICommandType]):
        command_id (Union[Unset, str]):
        is_visible (Union[Unset, bool]):
        is_enabled (Union[Unset, bool]):
        caption (Union[Unset, str]):
        set_focus (Union[Unset, bool]):
        confirmation_prompt (Union[Unset, str]):
    """

    command_type: Union[Unset, EmbyWebGenericUIModelEnumsUICommandType] = UNSET
    command_id: Union[Unset, str] = UNSET
    is_visible: Union[Unset, bool] = UNSET
    is_enabled: Union[Unset, bool] = UNSET
    caption: Union[Unset, str] = UNSET
    set_focus: Union[Unset, bool] = UNSET
    confirmation_prompt: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command_type: Union[Unset, str] = UNSET
        if not isinstance(self.command_type, Unset):
            command_type = self.command_type.value

        command_id = self.command_id
        is_visible = self.is_visible
        is_enabled = self.is_enabled
        caption = self.caption
        set_focus = self.set_focus
        confirmation_prompt = self.confirmation_prompt

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if command_type is not UNSET:
            field_dict["CommandType"] = command_type
        if command_id is not UNSET:
            field_dict["CommandId"] = command_id
        if is_visible is not UNSET:
            field_dict["IsVisible"] = is_visible
        if is_enabled is not UNSET:
            field_dict["IsEnabled"] = is_enabled
        if caption is not UNSET:
            field_dict["Caption"] = caption
        if set_focus is not UNSET:
            field_dict["SetFocus"] = set_focus
        if confirmation_prompt is not UNSET:
            field_dict["ConfirmationPrompt"] = confirmation_prompt

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _command_type = d.pop("CommandType", UNSET)
        command_type: Union[Unset, EmbyWebGenericUIModelEnumsUICommandType]
        if isinstance(_command_type, Unset):
            command_type = UNSET
        else:
            command_type = EmbyWebGenericUIModelEnumsUICommandType(_command_type)

        command_id = d.pop("CommandId", UNSET)

        is_visible = d.pop("IsVisible", UNSET)

        is_enabled = d.pop("IsEnabled", UNSET)

        caption = d.pop("Caption", UNSET)

        set_focus = d.pop("SetFocus", UNSET)

        confirmation_prompt = d.pop("ConfirmationPrompt", UNSET)

        emby_web_generic_ui_model_ui_command = cls(
            command_type=command_type,
            command_id=command_id,
            is_visible=is_visible,
            is_enabled=is_enabled,
            caption=caption,
            set_focus=set_focus,
            confirmation_prompt=confirmation_prompt,
        )

        emby_web_generic_ui_model_ui_command.additional_properties = d
        return emby_web_generic_ui_model_ui_command

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
