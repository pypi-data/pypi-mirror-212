from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BrandingBrandingOptions")


@attr.s(auto_attribs=True)
class BrandingBrandingOptions:
    """
    Attributes:
        login_disclaimer (Union[Unset, str]):
        custom_css (Union[Unset, str]):
    """

    login_disclaimer: Union[Unset, str] = UNSET
    custom_css: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        login_disclaimer = self.login_disclaimer
        custom_css = self.custom_css

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if login_disclaimer is not UNSET:
            field_dict["LoginDisclaimer"] = login_disclaimer
        if custom_css is not UNSET:
            field_dict["CustomCss"] = custom_css

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        login_disclaimer = d.pop("LoginDisclaimer", UNSET)

        custom_css = d.pop("CustomCss", UNSET)

        branding_branding_options = cls(
            login_disclaimer=login_disclaimer,
            custom_css=custom_css,
        )

        branding_branding_options.additional_properties = d
        return branding_branding_options

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
