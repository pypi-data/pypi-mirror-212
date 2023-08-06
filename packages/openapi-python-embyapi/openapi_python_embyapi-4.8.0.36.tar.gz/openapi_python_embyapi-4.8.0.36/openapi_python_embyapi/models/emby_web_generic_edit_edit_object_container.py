from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.emby_web_generic_edit_edit_object_container_default_object import (
        EmbyWebGenericEditEditObjectContainerDefaultObject,
    )
    from ..models.emby_web_generic_edit_edit_object_container_object import EmbyWebGenericEditEditObjectContainerObject
    from ..models.emby_web_generic_edit_editors_editor_root import EmbyWebGenericEditEditorsEditorRoot


T = TypeVar("T", bound="EmbyWebGenericEditEditObjectContainer")


@attr.s(auto_attribs=True)
class EmbyWebGenericEditEditObjectContainer:
    """
    Attributes:
        object_ (Union[Unset, EmbyWebGenericEditEditObjectContainerObject]):
        default_object (Union[Unset, EmbyWebGenericEditEditObjectContainerDefaultObject]):
        type_name (Union[Unset, str]):
        editor_root (Union[Unset, EmbyWebGenericEditEditorsEditorRoot]):
    """

    object_: Union[Unset, "EmbyWebGenericEditEditObjectContainerObject"] = UNSET
    default_object: Union[Unset, "EmbyWebGenericEditEditObjectContainerDefaultObject"] = UNSET
    type_name: Union[Unset, str] = UNSET
    editor_root: Union[Unset, "EmbyWebGenericEditEditorsEditorRoot"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.object_, Unset):
            object_ = self.object_.to_dict()

        default_object: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default_object, Unset):
            default_object = self.default_object.to_dict()

        type_name = self.type_name
        editor_root: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.editor_root, Unset):
            editor_root = self.editor_root.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_ is not UNSET:
            field_dict["Object"] = object_
        if default_object is not UNSET:
            field_dict["DefaultObject"] = default_object
        if type_name is not UNSET:
            field_dict["TypeName"] = type_name
        if editor_root is not UNSET:
            field_dict["EditorRoot"] = editor_root

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.emby_web_generic_edit_edit_object_container_default_object import (
            EmbyWebGenericEditEditObjectContainerDefaultObject,
        )
        from ..models.emby_web_generic_edit_edit_object_container_object import (
            EmbyWebGenericEditEditObjectContainerObject,
        )
        from ..models.emby_web_generic_edit_editors_editor_root import EmbyWebGenericEditEditorsEditorRoot

        d = src_dict.copy()
        _object_ = d.pop("Object", UNSET)
        object_: Union[Unset, EmbyWebGenericEditEditObjectContainerObject]
        if isinstance(_object_, Unset):
            object_ = UNSET
        else:
            object_ = EmbyWebGenericEditEditObjectContainerObject.from_dict(_object_)

        _default_object = d.pop("DefaultObject", UNSET)
        default_object: Union[Unset, EmbyWebGenericEditEditObjectContainerDefaultObject]
        if isinstance(_default_object, Unset):
            default_object = UNSET
        else:
            default_object = EmbyWebGenericEditEditObjectContainerDefaultObject.from_dict(_default_object)

        type_name = d.pop("TypeName", UNSET)

        _editor_root = d.pop("EditorRoot", UNSET)
        editor_root: Union[Unset, EmbyWebGenericEditEditorsEditorRoot]
        if isinstance(_editor_root, Unset):
            editor_root = UNSET
        else:
            editor_root = EmbyWebGenericEditEditorsEditorRoot.from_dict(_editor_root)

        emby_web_generic_edit_edit_object_container = cls(
            object_=object_,
            default_object=default_object,
            type_name=type_name,
            editor_root=editor_root,
        )

        emby_web_generic_edit_edit_object_container.additional_properties = d
        return emby_web_generic_edit_edit_object_container

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
