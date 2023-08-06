from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.marker_type import MarkerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChapterInfo")


@attr.s(auto_attribs=True)
class ChapterInfo:
    """
    Attributes:
        start_position_ticks (Union[Unset, int]):
        name (Union[Unset, str]):
        image_tag (Union[Unset, str]):
        marker_type (Union[Unset, MarkerType]):
        chapter_index (Union[Unset, int]):
    """

    start_position_ticks: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    image_tag: Union[Unset, str] = UNSET
    marker_type: Union[Unset, MarkerType] = UNSET
    chapter_index: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start_position_ticks = self.start_position_ticks
        name = self.name
        image_tag = self.image_tag
        marker_type: Union[Unset, str] = UNSET
        if not isinstance(self.marker_type, Unset):
            marker_type = self.marker_type.value

        chapter_index = self.chapter_index

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if start_position_ticks is not UNSET:
            field_dict["StartPositionTicks"] = start_position_ticks
        if name is not UNSET:
            field_dict["Name"] = name
        if image_tag is not UNSET:
            field_dict["ImageTag"] = image_tag
        if marker_type is not UNSET:
            field_dict["MarkerType"] = marker_type
        if chapter_index is not UNSET:
            field_dict["ChapterIndex"] = chapter_index

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start_position_ticks = d.pop("StartPositionTicks", UNSET)

        name = d.pop("Name", UNSET)

        image_tag = d.pop("ImageTag", UNSET)

        _marker_type = d.pop("MarkerType", UNSET)
        marker_type: Union[Unset, MarkerType]
        if isinstance(_marker_type, Unset):
            marker_type = UNSET
        else:
            marker_type = MarkerType(_marker_type)

        chapter_index = d.pop("ChapterIndex", UNSET)

        chapter_info = cls(
            start_position_ticks=start_position_ticks,
            name=name,
            image_tag=image_tag,
            marker_type=marker_type,
            chapter_index=chapter_index,
        )

        chapter_info.additional_properties = d
        return chapter_info

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
