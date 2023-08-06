from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmbyMediaModelTypesResolution")


@attr.s(auto_attribs=True)
class EmbyMediaModelTypesResolution:
    """
    Attributes:
        width (Union[Unset, int]):
        height (Union[Unset, int]):
    """

    width: Union[Unset, int] = UNSET
    height: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        width = self.width
        height = self.height

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if width is not UNSET:
            field_dict["Width"] = width
        if height is not UNSET:
            field_dict["Height"] = height

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        width = d.pop("Width", UNSET)

        height = d.pop("Height", UNSET)

        emby_media_model_types_resolution = cls(
            width=width,
            height=height,
        )

        emby_media_model_types_resolution.additional_properties = d
        return emby_media_model_types_resolution

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
