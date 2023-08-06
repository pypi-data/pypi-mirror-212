from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmbyMediaModelTypesProfileInformation")


@attr.s(auto_attribs=True)
class EmbyMediaModelTypesProfileInformation:
    """
    Attributes:
        short_name (Union[Unset, str]):
        description (Union[Unset, str]):
        details (Union[Unset, str]):
        id (Union[Unset, str]):
        bit_depths (Union[Unset, List[int]]):
    """

    short_name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    details: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    bit_depths: Union[Unset, List[int]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        short_name = self.short_name
        description = self.description
        details = self.details
        id = self.id
        bit_depths: Union[Unset, List[int]] = UNSET
        if not isinstance(self.bit_depths, Unset):
            bit_depths = self.bit_depths

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if short_name is not UNSET:
            field_dict["ShortName"] = short_name
        if description is not UNSET:
            field_dict["Description"] = description
        if details is not UNSET:
            field_dict["Details"] = details
        if id is not UNSET:
            field_dict["Id"] = id
        if bit_depths is not UNSET:
            field_dict["BitDepths"] = bit_depths

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        short_name = d.pop("ShortName", UNSET)

        description = d.pop("Description", UNSET)

        details = d.pop("Details", UNSET)

        id = d.pop("Id", UNSET)

        bit_depths = cast(List[int], d.pop("BitDepths", UNSET))

        emby_media_model_types_profile_information = cls(
            short_name=short_name,
            description=description,
            details=details,
            id=id,
            bit_depths=bit_depths,
        )

        emby_media_model_types_profile_information.additional_properties = d
        return emby_media_model_types_profile_information

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
