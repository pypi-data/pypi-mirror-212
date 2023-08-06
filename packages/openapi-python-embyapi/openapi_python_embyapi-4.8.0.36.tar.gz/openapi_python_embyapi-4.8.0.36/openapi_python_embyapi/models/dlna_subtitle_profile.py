from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dlna_subtitle_delivery_method import DlnaSubtitleDeliveryMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="DlnaSubtitleProfile")


@attr.s(auto_attribs=True)
class DlnaSubtitleProfile:
    """
    Attributes:
        format_ (Union[Unset, str]):
        method (Union[Unset, DlnaSubtitleDeliveryMethod]):
        didl_mode (Union[Unset, str]):
        language (Union[Unset, str]):
        container (Union[Unset, str]):
        protocol (Union[Unset, str]):
    """

    format_: Union[Unset, str] = UNSET
    method: Union[Unset, DlnaSubtitleDeliveryMethod] = UNSET
    didl_mode: Union[Unset, str] = UNSET
    language: Union[Unset, str] = UNSET
    container: Union[Unset, str] = UNSET
    protocol: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        format_ = self.format_
        method: Union[Unset, str] = UNSET
        if not isinstance(self.method, Unset):
            method = self.method.value

        didl_mode = self.didl_mode
        language = self.language
        container = self.container
        protocol = self.protocol

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if format_ is not UNSET:
            field_dict["Format"] = format_
        if method is not UNSET:
            field_dict["Method"] = method
        if didl_mode is not UNSET:
            field_dict["DidlMode"] = didl_mode
        if language is not UNSET:
            field_dict["Language"] = language
        if container is not UNSET:
            field_dict["Container"] = container
        if protocol is not UNSET:
            field_dict["Protocol"] = protocol

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        format_ = d.pop("Format", UNSET)

        _method = d.pop("Method", UNSET)
        method: Union[Unset, DlnaSubtitleDeliveryMethod]
        if isinstance(_method, Unset):
            method = UNSET
        else:
            method = DlnaSubtitleDeliveryMethod(_method)

        didl_mode = d.pop("DidlMode", UNSET)

        language = d.pop("Language", UNSET)

        container = d.pop("Container", UNSET)

        protocol = d.pop("Protocol", UNSET)

        dlna_subtitle_profile = cls(
            format_=format_,
            method=method,
            didl_mode=didl_mode,
            language=language,
            container=container,
            protocol=protocol,
        )

        dlna_subtitle_profile.additional_properties = d
        return dlna_subtitle_profile

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
