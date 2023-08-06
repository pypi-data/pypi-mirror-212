from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.image_type import ImageType
from ..models.rating_type import RatingType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RemoteImageInfo")


@attr.s(auto_attribs=True)
class RemoteImageInfo:
    """
    Attributes:
        provider_name (Union[Unset, str]):
        url (Union[Unset, str]):
        thumbnail_url (Union[Unset, str]):
        height (Union[Unset, None, int]):
        width (Union[Unset, None, int]):
        community_rating (Union[Unset, None, float]):
        vote_count (Union[Unset, None, int]):
        language (Union[Unset, str]):
        display_language (Union[Unset, str]):
        type (Union[Unset, ImageType]):
        rating_type (Union[Unset, RatingType]):
    """

    provider_name: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    thumbnail_url: Union[Unset, str] = UNSET
    height: Union[Unset, None, int] = UNSET
    width: Union[Unset, None, int] = UNSET
    community_rating: Union[Unset, None, float] = UNSET
    vote_count: Union[Unset, None, int] = UNSET
    language: Union[Unset, str] = UNSET
    display_language: Union[Unset, str] = UNSET
    type: Union[Unset, ImageType] = UNSET
    rating_type: Union[Unset, RatingType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        provider_name = self.provider_name
        url = self.url
        thumbnail_url = self.thumbnail_url
        height = self.height
        width = self.width
        community_rating = self.community_rating
        vote_count = self.vote_count
        language = self.language
        display_language = self.display_language
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        rating_type: Union[Unset, str] = UNSET
        if not isinstance(self.rating_type, Unset):
            rating_type = self.rating_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if provider_name is not UNSET:
            field_dict["ProviderName"] = provider_name
        if url is not UNSET:
            field_dict["Url"] = url
        if thumbnail_url is not UNSET:
            field_dict["ThumbnailUrl"] = thumbnail_url
        if height is not UNSET:
            field_dict["Height"] = height
        if width is not UNSET:
            field_dict["Width"] = width
        if community_rating is not UNSET:
            field_dict["CommunityRating"] = community_rating
        if vote_count is not UNSET:
            field_dict["VoteCount"] = vote_count
        if language is not UNSET:
            field_dict["Language"] = language
        if display_language is not UNSET:
            field_dict["DisplayLanguage"] = display_language
        if type is not UNSET:
            field_dict["Type"] = type
        if rating_type is not UNSET:
            field_dict["RatingType"] = rating_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        provider_name = d.pop("ProviderName", UNSET)

        url = d.pop("Url", UNSET)

        thumbnail_url = d.pop("ThumbnailUrl", UNSET)

        height = d.pop("Height", UNSET)

        width = d.pop("Width", UNSET)

        community_rating = d.pop("CommunityRating", UNSET)

        vote_count = d.pop("VoteCount", UNSET)

        language = d.pop("Language", UNSET)

        display_language = d.pop("DisplayLanguage", UNSET)

        _type = d.pop("Type", UNSET)
        type: Union[Unset, ImageType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = ImageType(_type)

        _rating_type = d.pop("RatingType", UNSET)
        rating_type: Union[Unset, RatingType]
        if isinstance(_rating_type, Unset):
            rating_type = UNSET
        else:
            rating_type = RatingType(_rating_type)

        remote_image_info = cls(
            provider_name=provider_name,
            url=url,
            thumbnail_url=thumbnail_url,
            height=height,
            width=width,
            community_rating=community_rating,
            vote_count=vote_count,
            language=language,
            display_language=display_language,
            type=type,
            rating_type=rating_type,
        )

        remote_image_info.additional_properties = d
        return remote_image_info

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
