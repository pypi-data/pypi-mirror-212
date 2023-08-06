from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.image_type import ImageType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ImageInfo")


@attr.s(auto_attribs=True)
class ImageInfo:
    """
    Attributes:
        image_type (Union[Unset, ImageType]):
        image_index (Union[Unset, None, int]):
        path (Union[Unset, str]):
        filename (Union[Unset, str]):
        height (Union[Unset, None, int]):
        width (Union[Unset, None, int]):
        size (Union[Unset, int]):
    """

    image_type: Union[Unset, ImageType] = UNSET
    image_index: Union[Unset, None, int] = UNSET
    path: Union[Unset, str] = UNSET
    filename: Union[Unset, str] = UNSET
    height: Union[Unset, None, int] = UNSET
    width: Union[Unset, None, int] = UNSET
    size: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        image_type: Union[Unset, str] = UNSET
        if not isinstance(self.image_type, Unset):
            image_type = self.image_type.value

        image_index = self.image_index
        path = self.path
        filename = self.filename
        height = self.height
        width = self.width
        size = self.size

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if image_type is not UNSET:
            field_dict["ImageType"] = image_type
        if image_index is not UNSET:
            field_dict["ImageIndex"] = image_index
        if path is not UNSET:
            field_dict["Path"] = path
        if filename is not UNSET:
            field_dict["Filename"] = filename
        if height is not UNSET:
            field_dict["Height"] = height
        if width is not UNSET:
            field_dict["Width"] = width
        if size is not UNSET:
            field_dict["Size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _image_type = d.pop("ImageType", UNSET)
        image_type: Union[Unset, ImageType]
        if isinstance(_image_type, Unset):
            image_type = UNSET
        else:
            image_type = ImageType(_image_type)

        image_index = d.pop("ImageIndex", UNSET)

        path = d.pop("Path", UNSET)

        filename = d.pop("Filename", UNSET)

        height = d.pop("Height", UNSET)

        width = d.pop("Width", UNSET)

        size = d.pop("Size", UNSET)

        image_info = cls(
            image_type=image_type,
            image_index=image_index,
            path=path,
            filename=filename,
            height=height,
            width=width,
            size=size,
        )

        image_info.additional_properties = d
        return image_info

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
