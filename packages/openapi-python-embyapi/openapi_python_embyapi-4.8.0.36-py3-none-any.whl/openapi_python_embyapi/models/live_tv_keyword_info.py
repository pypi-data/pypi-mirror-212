from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.live_tv_keyword_type import LiveTvKeywordType
from ..types import UNSET, Unset

T = TypeVar("T", bound="LiveTvKeywordInfo")


@attr.s(auto_attribs=True)
class LiveTvKeywordInfo:
    """
    Attributes:
        keyword_type (Union[Unset, LiveTvKeywordType]):
        keyword (Union[Unset, str]):
    """

    keyword_type: Union[Unset, LiveTvKeywordType] = UNSET
    keyword: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        keyword_type: Union[Unset, str] = UNSET
        if not isinstance(self.keyword_type, Unset):
            keyword_type = self.keyword_type.value

        keyword = self.keyword

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if keyword_type is not UNSET:
            field_dict["KeywordType"] = keyword_type
        if keyword is not UNSET:
            field_dict["Keyword"] = keyword

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _keyword_type = d.pop("KeywordType", UNSET)
        keyword_type: Union[Unset, LiveTvKeywordType]
        if isinstance(_keyword_type, Unset):
            keyword_type = UNSET
        else:
            keyword_type = LiveTvKeywordType(_keyword_type)

        keyword = d.pop("Keyword", UNSET)

        live_tv_keyword_info = cls(
            keyword_type=keyword_type,
            keyword=keyword,
        )

        live_tv_keyword_info.additional_properties = d
        return live_tv_keyword_info

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
