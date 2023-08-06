from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RokuMetadataApiThumbnailInfo")


@attr.s(auto_attribs=True)
class RokuMetadataApiThumbnailInfo:
    """
    Attributes:
        position_ticks (Union[Unset, int]):
        image_tag (Union[Unset, str]):
    """

    position_ticks: Union[Unset, int] = UNSET
    image_tag: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        position_ticks = self.position_ticks
        image_tag = self.image_tag

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if position_ticks is not UNSET:
            field_dict["PositionTicks"] = position_ticks
        if image_tag is not UNSET:
            field_dict["ImageTag"] = image_tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        position_ticks = d.pop("PositionTicks", UNSET)

        image_tag = d.pop("ImageTag", UNSET)

        roku_metadata_api_thumbnail_info = cls(
            position_ticks=position_ticks,
            image_tag=image_tag,
        )

        roku_metadata_api_thumbnail_info.additional_properties = d
        return roku_metadata_api_thumbnail_info

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
