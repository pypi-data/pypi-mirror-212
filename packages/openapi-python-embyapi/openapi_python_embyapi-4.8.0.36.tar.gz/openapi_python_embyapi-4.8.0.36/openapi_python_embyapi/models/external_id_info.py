from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExternalIdInfo")


@attr.s(auto_attribs=True)
class ExternalIdInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        key (Union[Unset, str]):
        url_format_string (Union[Unset, str]):
        is_supported_as_identifier (Union[Unset, bool]):
    """

    name: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    url_format_string: Union[Unset, str] = UNSET
    is_supported_as_identifier: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        key = self.key
        url_format_string = self.url_format_string
        is_supported_as_identifier = self.is_supported_as_identifier

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if key is not UNSET:
            field_dict["Key"] = key
        if url_format_string is not UNSET:
            field_dict["UrlFormatString"] = url_format_string
        if is_supported_as_identifier is not UNSET:
            field_dict["IsSupportedAsIdentifier"] = is_supported_as_identifier

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        key = d.pop("Key", UNSET)

        url_format_string = d.pop("UrlFormatString", UNSET)

        is_supported_as_identifier = d.pop("IsSupportedAsIdentifier", UNSET)

        external_id_info = cls(
            name=name,
            key=key,
            url_format_string=url_format_string,
            is_supported_as_identifier=is_supported_as_identifier,
        )

        external_id_info.additional_properties = d
        return external_id_info

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
