from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GlobalizationCultureDto")


@attr.s(auto_attribs=True)
class GlobalizationCultureDto:
    """
    Attributes:
        name (Union[Unset, str]):
        display_name (Union[Unset, str]):
        two_letter_iso_language_name (Union[Unset, str]):
        three_letter_iso_language_name (Union[Unset, str]):
        three_letter_iso_language_names (Union[Unset, List[str]]):
        two_letter_iso_language_names (Union[Unset, List[str]]):
    """

    name: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    two_letter_iso_language_name: Union[Unset, str] = UNSET
    three_letter_iso_language_name: Union[Unset, str] = UNSET
    three_letter_iso_language_names: Union[Unset, List[str]] = UNSET
    two_letter_iso_language_names: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        display_name = self.display_name
        two_letter_iso_language_name = self.two_letter_iso_language_name
        three_letter_iso_language_name = self.three_letter_iso_language_name
        three_letter_iso_language_names: Union[Unset, List[str]] = UNSET
        if not isinstance(self.three_letter_iso_language_names, Unset):
            three_letter_iso_language_names = self.three_letter_iso_language_names

        two_letter_iso_language_names: Union[Unset, List[str]] = UNSET
        if not isinstance(self.two_letter_iso_language_names, Unset):
            two_letter_iso_language_names = self.two_letter_iso_language_names

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if display_name is not UNSET:
            field_dict["DisplayName"] = display_name
        if two_letter_iso_language_name is not UNSET:
            field_dict["TwoLetterISOLanguageName"] = two_letter_iso_language_name
        if three_letter_iso_language_name is not UNSET:
            field_dict["ThreeLetterISOLanguageName"] = three_letter_iso_language_name
        if three_letter_iso_language_names is not UNSET:
            field_dict["ThreeLetterISOLanguageNames"] = three_letter_iso_language_names
        if two_letter_iso_language_names is not UNSET:
            field_dict["TwoLetterISOLanguageNames"] = two_letter_iso_language_names

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        display_name = d.pop("DisplayName", UNSET)

        two_letter_iso_language_name = d.pop("TwoLetterISOLanguageName", UNSET)

        three_letter_iso_language_name = d.pop("ThreeLetterISOLanguageName", UNSET)

        three_letter_iso_language_names = cast(List[str], d.pop("ThreeLetterISOLanguageNames", UNSET))

        two_letter_iso_language_names = cast(List[str], d.pop("TwoLetterISOLanguageNames", UNSET))

        globalization_culture_dto = cls(
            name=name,
            display_name=display_name,
            two_letter_iso_language_name=two_letter_iso_language_name,
            three_letter_iso_language_name=three_letter_iso_language_name,
            three_letter_iso_language_names=three_letter_iso_language_names,
            two_letter_iso_language_names=two_letter_iso_language_names,
        )

        globalization_culture_dto.additional_properties = d
        return globalization_culture_dto

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
