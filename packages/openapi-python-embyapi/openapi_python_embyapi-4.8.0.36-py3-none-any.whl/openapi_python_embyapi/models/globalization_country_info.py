from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GlobalizationCountryInfo")


@attr.s(auto_attribs=True)
class GlobalizationCountryInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        display_name (Union[Unset, str]):
        english_name (Union[Unset, str]):
        two_letter_iso_region_name (Union[Unset, str]):
        three_letter_iso_region_name (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    english_name: Union[Unset, str] = UNSET
    two_letter_iso_region_name: Union[Unset, str] = UNSET
    three_letter_iso_region_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        display_name = self.display_name
        english_name = self.english_name
        two_letter_iso_region_name = self.two_letter_iso_region_name
        three_letter_iso_region_name = self.three_letter_iso_region_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if display_name is not UNSET:
            field_dict["DisplayName"] = display_name
        if english_name is not UNSET:
            field_dict["EnglishName"] = english_name
        if two_letter_iso_region_name is not UNSET:
            field_dict["TwoLetterISORegionName"] = two_letter_iso_region_name
        if three_letter_iso_region_name is not UNSET:
            field_dict["ThreeLetterISORegionName"] = three_letter_iso_region_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        display_name = d.pop("DisplayName", UNSET)

        english_name = d.pop("EnglishName", UNSET)

        two_letter_iso_region_name = d.pop("TwoLetterISORegionName", UNSET)

        three_letter_iso_region_name = d.pop("ThreeLetterISORegionName", UNSET)

        globalization_country_info = cls(
            name=name,
            display_name=display_name,
            english_name=english_name,
            two_letter_iso_region_name=two_letter_iso_region_name,
            three_letter_iso_region_name=three_letter_iso_region_name,
        )

        globalization_country_info.additional_properties = d
        return globalization_country_info

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
