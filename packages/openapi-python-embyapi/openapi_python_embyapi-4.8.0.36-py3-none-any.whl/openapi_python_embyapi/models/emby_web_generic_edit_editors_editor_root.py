from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.emby_web_generic_edit_common_editor_types import EmbyWebGenericEditCommonEditorTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.emby_web_generic_edit_actions_postback_action import EmbyWebGenericEditActionsPostbackAction
    from ..models.emby_web_generic_edit_conditions_property_condition import (
        EmbyWebGenericEditConditionsPropertyCondition,
    )
    from ..models.emby_web_generic_edit_editors_editor_base import EmbyWebGenericEditEditorsEditorBase
    from ..models.emby_web_generic_edit_editors_editor_button_item import EmbyWebGenericEditEditorsEditorButtonItem


T = TypeVar("T", bound="EmbyWebGenericEditEditorsEditorRoot")


@attr.s(auto_attribs=True)
class EmbyWebGenericEditEditorsEditorRoot:
    """
    Attributes:
        property_conditions (Union[Unset, List['EmbyWebGenericEditConditionsPropertyCondition']]):
        postback_actions (Union[Unset, List['EmbyWebGenericEditActionsPostbackAction']]):
        title_button (Union[Unset, EmbyWebGenericEditEditorsEditorButtonItem]):
        editor_items (Union[Unset, List['EmbyWebGenericEditEditorsEditorBase']]):
        editor_type (Union[Unset, EmbyWebGenericEditCommonEditorTypes]):
        name (Union[Unset, str]):
        id (Union[Unset, str]):
        allow_empty (Union[Unset, bool]):
        is_read_only (Union[Unset, bool]):
        is_advanced (Union[Unset, bool]):
        display_name (Union[Unset, str]):
        description (Union[Unset, str]):
        parent_id (Union[Unset, str]):
    """

    property_conditions: Union[Unset, List["EmbyWebGenericEditConditionsPropertyCondition"]] = UNSET
    postback_actions: Union[Unset, List["EmbyWebGenericEditActionsPostbackAction"]] = UNSET
    title_button: Union[Unset, "EmbyWebGenericEditEditorsEditorButtonItem"] = UNSET
    editor_items: Union[Unset, List["EmbyWebGenericEditEditorsEditorBase"]] = UNSET
    editor_type: Union[Unset, EmbyWebGenericEditCommonEditorTypes] = UNSET
    name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    allow_empty: Union[Unset, bool] = UNSET
    is_read_only: Union[Unset, bool] = UNSET
    is_advanced: Union[Unset, bool] = UNSET
    display_name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    parent_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        property_conditions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.property_conditions, Unset):
            property_conditions = []
            for property_conditions_item_data in self.property_conditions:
                property_conditions_item = property_conditions_item_data.to_dict()

                property_conditions.append(property_conditions_item)

        postback_actions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.postback_actions, Unset):
            postback_actions = []
            for postback_actions_item_data in self.postback_actions:
                postback_actions_item = postback_actions_item_data.to_dict()

                postback_actions.append(postback_actions_item)

        title_button: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.title_button, Unset):
            title_button = self.title_button.to_dict()

        editor_items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.editor_items, Unset):
            editor_items = []
            for editor_items_item_data in self.editor_items:
                editor_items_item = editor_items_item_data.to_dict()

                editor_items.append(editor_items_item)

        editor_type: Union[Unset, str] = UNSET
        if not isinstance(self.editor_type, Unset):
            editor_type = self.editor_type.value

        name = self.name
        id = self.id
        allow_empty = self.allow_empty
        is_read_only = self.is_read_only
        is_advanced = self.is_advanced
        display_name = self.display_name
        description = self.description
        parent_id = self.parent_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if property_conditions is not UNSET:
            field_dict["PropertyConditions"] = property_conditions
        if postback_actions is not UNSET:
            field_dict["PostbackActions"] = postback_actions
        if title_button is not UNSET:
            field_dict["TitleButton"] = title_button
        if editor_items is not UNSET:
            field_dict["EditorItems"] = editor_items
        if editor_type is not UNSET:
            field_dict["EditorType"] = editor_type
        if name is not UNSET:
            field_dict["Name"] = name
        if id is not UNSET:
            field_dict["Id"] = id
        if allow_empty is not UNSET:
            field_dict["AllowEmpty"] = allow_empty
        if is_read_only is not UNSET:
            field_dict["IsReadOnly"] = is_read_only
        if is_advanced is not UNSET:
            field_dict["IsAdvanced"] = is_advanced
        if display_name is not UNSET:
            field_dict["DisplayName"] = display_name
        if description is not UNSET:
            field_dict["Description"] = description
        if parent_id is not UNSET:
            field_dict["ParentId"] = parent_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.emby_web_generic_edit_actions_postback_action import EmbyWebGenericEditActionsPostbackAction
        from ..models.emby_web_generic_edit_conditions_property_condition import (
            EmbyWebGenericEditConditionsPropertyCondition,
        )
        from ..models.emby_web_generic_edit_editors_editor_base import EmbyWebGenericEditEditorsEditorBase
        from ..models.emby_web_generic_edit_editors_editor_button_item import EmbyWebGenericEditEditorsEditorButtonItem

        d = src_dict.copy()
        property_conditions = []
        _property_conditions = d.pop("PropertyConditions", UNSET)
        for property_conditions_item_data in _property_conditions or []:
            property_conditions_item = EmbyWebGenericEditConditionsPropertyCondition.from_dict(
                property_conditions_item_data
            )

            property_conditions.append(property_conditions_item)

        postback_actions = []
        _postback_actions = d.pop("PostbackActions", UNSET)
        for postback_actions_item_data in _postback_actions or []:
            postback_actions_item = EmbyWebGenericEditActionsPostbackAction.from_dict(postback_actions_item_data)

            postback_actions.append(postback_actions_item)

        _title_button = d.pop("TitleButton", UNSET)
        title_button: Union[Unset, EmbyWebGenericEditEditorsEditorButtonItem]
        if isinstance(_title_button, Unset):
            title_button = UNSET
        else:
            title_button = EmbyWebGenericEditEditorsEditorButtonItem.from_dict(_title_button)

        editor_items = []
        _editor_items = d.pop("EditorItems", UNSET)
        for editor_items_item_data in _editor_items or []:
            editor_items_item = EmbyWebGenericEditEditorsEditorBase.from_dict(editor_items_item_data)

            editor_items.append(editor_items_item)

        _editor_type = d.pop("EditorType", UNSET)
        editor_type: Union[Unset, EmbyWebGenericEditCommonEditorTypes]
        if isinstance(_editor_type, Unset):
            editor_type = UNSET
        else:
            editor_type = EmbyWebGenericEditCommonEditorTypes(_editor_type)

        name = d.pop("Name", UNSET)

        id = d.pop("Id", UNSET)

        allow_empty = d.pop("AllowEmpty", UNSET)

        is_read_only = d.pop("IsReadOnly", UNSET)

        is_advanced = d.pop("IsAdvanced", UNSET)

        display_name = d.pop("DisplayName", UNSET)

        description = d.pop("Description", UNSET)

        parent_id = d.pop("ParentId", UNSET)

        emby_web_generic_edit_editors_editor_root = cls(
            property_conditions=property_conditions,
            postback_actions=postback_actions,
            title_button=title_button,
            editor_items=editor_items,
            editor_type=editor_type,
            name=name,
            id=id,
            allow_empty=allow_empty,
            is_read_only=is_read_only,
            is_advanced=is_advanced,
            display_name=display_name,
            description=description,
            parent_id=parent_id,
        )

        emby_web_generic_edit_editors_editor_root.additional_properties = d
        return emby_web_generic_edit_editors_editor_root

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
