from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.generic_edit_i_edit_object_container_default_object import (
        GenericEditIEditObjectContainerDefaultObject,
    )
    from ..models.generic_edit_i_edit_object_container_object import GenericEditIEditObjectContainerObject


T = TypeVar("T", bound="GenericEditIEditObjectContainer")


@attr.s(auto_attribs=True)
class GenericEditIEditObjectContainer:
    """
    Attributes:
        object_ (Union[Unset, GenericEditIEditObjectContainerObject]):
        default_object (Union[Unset, GenericEditIEditObjectContainerDefaultObject]):
        type_name (Union[Unset, str]):
    """

    object_: Union[Unset, "GenericEditIEditObjectContainerObject"] = UNSET
    default_object: Union[Unset, "GenericEditIEditObjectContainerDefaultObject"] = UNSET
    type_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.object_, Unset):
            object_ = self.object_.to_dict()

        default_object: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default_object, Unset):
            default_object = self.default_object.to_dict()

        type_name = self.type_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_ is not UNSET:
            field_dict["Object"] = object_
        if default_object is not UNSET:
            field_dict["DefaultObject"] = default_object
        if type_name is not UNSET:
            field_dict["TypeName"] = type_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.generic_edit_i_edit_object_container_default_object import (
            GenericEditIEditObjectContainerDefaultObject,
        )
        from ..models.generic_edit_i_edit_object_container_object import GenericEditIEditObjectContainerObject

        d = src_dict.copy()
        _object_ = d.pop("Object", UNSET)
        object_: Union[Unset, GenericEditIEditObjectContainerObject]
        if isinstance(_object_, Unset):
            object_ = UNSET
        else:
            object_ = GenericEditIEditObjectContainerObject.from_dict(_object_)

        _default_object = d.pop("DefaultObject", UNSET)
        default_object: Union[Unset, GenericEditIEditObjectContainerDefaultObject]
        if isinstance(_default_object, Unset):
            default_object = UNSET
        else:
            default_object = GenericEditIEditObjectContainerDefaultObject.from_dict(_default_object)

        type_name = d.pop("TypeName", UNSET)

        generic_edit_i_edit_object_container = cls(
            object_=object_,
            default_object=default_object,
            type_name=type_name,
        )

        generic_edit_i_edit_object_container.additional_properties = d
        return generic_edit_i_edit_object_container

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
