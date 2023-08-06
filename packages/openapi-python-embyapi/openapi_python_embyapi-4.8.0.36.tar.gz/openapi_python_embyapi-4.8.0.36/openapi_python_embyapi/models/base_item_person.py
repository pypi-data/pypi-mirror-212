from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.person_type import PersonType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseItemPerson")


@attr.s(auto_attribs=True)
class BaseItemPerson:
    """
    Attributes:
        name (Union[Unset, str]):
        id (Union[Unset, str]):
        role (Union[Unset, str]):
        type (Union[Unset, PersonType]):
        primary_image_tag (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    role: Union[Unset, str] = UNSET
    type: Union[Unset, PersonType] = UNSET
    primary_image_tag: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        role = self.role
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        primary_image_tag = self.primary_image_tag

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if id is not UNSET:
            field_dict["Id"] = id
        if role is not UNSET:
            field_dict["Role"] = role
        if type is not UNSET:
            field_dict["Type"] = type
        if primary_image_tag is not UNSET:
            field_dict["PrimaryImageTag"] = primary_image_tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        id = d.pop("Id", UNSET)

        role = d.pop("Role", UNSET)

        _type = d.pop("Type", UNSET)
        type: Union[Unset, PersonType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = PersonType(_type)

        primary_image_tag = d.pop("PrimaryImageTag", UNSET)

        base_item_person = cls(
            name=name,
            id=id,
            role=role,
            type=type,
            primary_image_tag=primary_image_tag,
        )

        base_item_person.additional_properties = d
        return base_item_person

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
