from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.image_type import ImageType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ImageProviderInfo")


@attr.s(auto_attribs=True)
class ImageProviderInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        supported_images (Union[Unset, List[ImageType]]):
    """

    name: Union[Unset, str] = UNSET
    supported_images: Union[Unset, List[ImageType]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        supported_images: Union[Unset, List[str]] = UNSET
        if not isinstance(self.supported_images, Unset):
            supported_images = []
            for supported_images_item_data in self.supported_images:
                supported_images_item = supported_images_item_data.value

                supported_images.append(supported_images_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if supported_images is not UNSET:
            field_dict["SupportedImages"] = supported_images

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        supported_images = []
        _supported_images = d.pop("SupportedImages", UNSET)
        for supported_images_item_data in _supported_images or []:
            supported_images_item = ImageType(supported_images_item_data)

            supported_images.append(supported_images_item)

        image_provider_info = cls(
            name=name,
            supported_images=supported_images,
        )

        image_provider_info.additional_properties = d
        return image_provider_info

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
