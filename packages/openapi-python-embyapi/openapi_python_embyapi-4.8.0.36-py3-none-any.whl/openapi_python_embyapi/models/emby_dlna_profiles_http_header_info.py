from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.emby_dlna_profiles_header_match_type import EmbyDlnaProfilesHeaderMatchType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmbyDlnaProfilesHttpHeaderInfo")


@attr.s(auto_attribs=True)
class EmbyDlnaProfilesHttpHeaderInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        value (Union[Unset, str]):
        match (Union[Unset, EmbyDlnaProfilesHeaderMatchType]):
    """

    name: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    match: Union[Unset, EmbyDlnaProfilesHeaderMatchType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        value = self.value
        match: Union[Unset, str] = UNSET
        if not isinstance(self.match, Unset):
            match = self.match.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if value is not UNSET:
            field_dict["Value"] = value
        if match is not UNSET:
            field_dict["Match"] = match

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        value = d.pop("Value", UNSET)

        _match = d.pop("Match", UNSET)
        match: Union[Unset, EmbyDlnaProfilesHeaderMatchType]
        if isinstance(_match, Unset):
            match = UNSET
        else:
            match = EmbyDlnaProfilesHeaderMatchType(_match)

        emby_dlna_profiles_http_header_info = cls(
            name=name,
            value=value,
            match=match,
        )

        emby_dlna_profiles_http_header_info.additional_properties = d
        return emby_dlna_profiles_http_header_info

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
