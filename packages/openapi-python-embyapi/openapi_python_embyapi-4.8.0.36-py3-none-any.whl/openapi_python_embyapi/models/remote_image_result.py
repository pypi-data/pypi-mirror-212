from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.remote_image_info import RemoteImageInfo


T = TypeVar("T", bound="RemoteImageResult")


@attr.s(auto_attribs=True)
class RemoteImageResult:
    """
    Attributes:
        images (Union[Unset, List['RemoteImageInfo']]):
        total_record_count (Union[Unset, int]):
        providers (Union[Unset, List[str]]):
    """

    images: Union[Unset, List["RemoteImageInfo"]] = UNSET
    total_record_count: Union[Unset, int] = UNSET
    providers: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        images: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.images, Unset):
            images = []
            for images_item_data in self.images:
                images_item = images_item_data.to_dict()

                images.append(images_item)

        total_record_count = self.total_record_count
        providers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.providers, Unset):
            providers = self.providers

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if images is not UNSET:
            field_dict["Images"] = images
        if total_record_count is not UNSET:
            field_dict["TotalRecordCount"] = total_record_count
        if providers is not UNSET:
            field_dict["Providers"] = providers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.remote_image_info import RemoteImageInfo

        d = src_dict.copy()
        images = []
        _images = d.pop("Images", UNSET)
        for images_item_data in _images or []:
            images_item = RemoteImageInfo.from_dict(images_item_data)

            images.append(images_item)

        total_record_count = d.pop("TotalRecordCount", UNSET)

        providers = cast(List[str], d.pop("Providers", UNSET))

        remote_image_result = cls(
            images=images,
            total_record_count=total_record_count,
            providers=providers,
        )

        remote_image_result.additional_properties = d
        return remote_image_result

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
