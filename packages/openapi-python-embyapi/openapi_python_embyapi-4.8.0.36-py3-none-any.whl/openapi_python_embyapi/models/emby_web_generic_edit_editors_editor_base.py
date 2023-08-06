from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.emby_web_generic_edit_common_editor_types import EmbyWebGenericEditCommonEditorTypes
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmbyWebGenericEditEditorsEditorBase")


@attr.s(auto_attribs=True)
class EmbyWebGenericEditEditorsEditorBase:
    """
    Attributes:
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
        d = src_dict.copy()
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

        emby_web_generic_edit_editors_editor_base = cls(
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

        emby_web_generic_edit_editors_editor_base.additional_properties = d
        return emby_web_generic_edit_editors_editor_base

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
