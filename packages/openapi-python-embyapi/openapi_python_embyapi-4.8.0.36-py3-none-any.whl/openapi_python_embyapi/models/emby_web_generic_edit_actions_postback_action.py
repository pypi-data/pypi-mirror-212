from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmbyWebGenericEditActionsPostbackAction")


@attr.s(auto_attribs=True)
class EmbyWebGenericEditActionsPostbackAction:
    """
    Attributes:
        target_editor_id (Union[Unset, str]):
        postback_command_id (Union[Unset, str]):
        command_parameter_property_id (Union[Unset, str]):
    """

    target_editor_id: Union[Unset, str] = UNSET
    postback_command_id: Union[Unset, str] = UNSET
    command_parameter_property_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        target_editor_id = self.target_editor_id
        postback_command_id = self.postback_command_id
        command_parameter_property_id = self.command_parameter_property_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if target_editor_id is not UNSET:
            field_dict["TargetEditorId"] = target_editor_id
        if postback_command_id is not UNSET:
            field_dict["PostbackCommandId"] = postback_command_id
        if command_parameter_property_id is not UNSET:
            field_dict["CommandParameterPropertyId"] = command_parameter_property_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        target_editor_id = d.pop("TargetEditorId", UNSET)

        postback_command_id = d.pop("PostbackCommandId", UNSET)

        command_parameter_property_id = d.pop("CommandParameterPropertyId", UNSET)

        emby_web_generic_edit_actions_postback_action = cls(
            target_editor_id=target_editor_id,
            postback_command_id=postback_command_id,
            command_parameter_property_id=command_parameter_property_id,
        )

        emby_web_generic_edit_actions_postback_action.additional_properties = d
        return emby_web_generic_edit_actions_postback_action

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
