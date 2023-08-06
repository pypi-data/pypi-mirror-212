from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.image_type import ImageType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConfigurationImageOption")


@attr.s(auto_attribs=True)
class ConfigurationImageOption:
    """
    Attributes:
        type (Union[Unset, ImageType]):
        limit (Union[Unset, int]):
        min_width (Union[Unset, int]):
    """

    type: Union[Unset, ImageType] = UNSET
    limit: Union[Unset, int] = UNSET
    min_width: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        limit = self.limit
        min_width = self.min_width

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["Type"] = type
        if limit is not UNSET:
            field_dict["Limit"] = limit
        if min_width is not UNSET:
            field_dict["MinWidth"] = min_width

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("Type", UNSET)
        type: Union[Unset, ImageType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = ImageType(_type)

        limit = d.pop("Limit", UNSET)

        min_width = d.pop("MinWidth", UNSET)

        configuration_image_option = cls(
            type=type,
            limit=limit,
            min_width=min_width,
        )

        configuration_image_option.additional_properties = d
        return configuration_image_option

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
