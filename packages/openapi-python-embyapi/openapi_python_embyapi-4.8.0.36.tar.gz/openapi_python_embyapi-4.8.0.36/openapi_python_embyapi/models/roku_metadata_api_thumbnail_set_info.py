from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.roku_metadata_api_thumbnail_info import RokuMetadataApiThumbnailInfo


T = TypeVar("T", bound="RokuMetadataApiThumbnailSetInfo")


@attr.s(auto_attribs=True)
class RokuMetadataApiThumbnailSetInfo:
    """
    Attributes:
        aspect_ratio (Union[Unset, None, float]):
        thumbnails (Union[Unset, List['RokuMetadataApiThumbnailInfo']]):
    """

    aspect_ratio: Union[Unset, None, float] = UNSET
    thumbnails: Union[Unset, List["RokuMetadataApiThumbnailInfo"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        aspect_ratio = self.aspect_ratio
        thumbnails: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.thumbnails, Unset):
            thumbnails = []
            for thumbnails_item_data in self.thumbnails:
                thumbnails_item = thumbnails_item_data.to_dict()

                thumbnails.append(thumbnails_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aspect_ratio is not UNSET:
            field_dict["AspectRatio"] = aspect_ratio
        if thumbnails is not UNSET:
            field_dict["Thumbnails"] = thumbnails

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.roku_metadata_api_thumbnail_info import RokuMetadataApiThumbnailInfo

        d = src_dict.copy()
        aspect_ratio = d.pop("AspectRatio", UNSET)

        thumbnails = []
        _thumbnails = d.pop("Thumbnails", UNSET)
        for thumbnails_item_data in _thumbnails or []:
            thumbnails_item = RokuMetadataApiThumbnailInfo.from_dict(thumbnails_item_data)

            thumbnails.append(thumbnails_item)

        roku_metadata_api_thumbnail_set_info = cls(
            aspect_ratio=aspect_ratio,
            thumbnails=thumbnails,
        )

        roku_metadata_api_thumbnail_set_info.additional_properties = d
        return roku_metadata_api_thumbnail_set_info

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
