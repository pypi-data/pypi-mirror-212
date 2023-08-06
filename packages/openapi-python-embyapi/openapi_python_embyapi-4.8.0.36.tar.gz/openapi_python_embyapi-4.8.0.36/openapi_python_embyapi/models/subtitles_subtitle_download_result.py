from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubtitlesSubtitleDownloadResult")


@attr.s(auto_attribs=True)
class SubtitlesSubtitleDownloadResult:
    """
    Attributes:
        new_index (Union[Unset, None, int]):
    """

    new_index: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        new_index = self.new_index

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if new_index is not UNSET:
            field_dict["NewIndex"] = new_index

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        new_index = d.pop("NewIndex", UNSET)

        subtitles_subtitle_download_result = cls(
            new_index=new_index,
        )

        subtitles_subtitle_download_result.additional_properties = d
        return subtitles_subtitle_download_result

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
