from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.theme_media_result import ThemeMediaResult


T = TypeVar("T", bound="AllThemeMediaResult")


@attr.s(auto_attribs=True)
class AllThemeMediaResult:
    """
    Attributes:
        theme_videos_result (Union[Unset, ThemeMediaResult]):
        theme_songs_result (Union[Unset, ThemeMediaResult]):
        soundtrack_songs_result (Union[Unset, ThemeMediaResult]):
    """

    theme_videos_result: Union[Unset, "ThemeMediaResult"] = UNSET
    theme_songs_result: Union[Unset, "ThemeMediaResult"] = UNSET
    soundtrack_songs_result: Union[Unset, "ThemeMediaResult"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        theme_videos_result: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.theme_videos_result, Unset):
            theme_videos_result = self.theme_videos_result.to_dict()

        theme_songs_result: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.theme_songs_result, Unset):
            theme_songs_result = self.theme_songs_result.to_dict()

        soundtrack_songs_result: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.soundtrack_songs_result, Unset):
            soundtrack_songs_result = self.soundtrack_songs_result.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if theme_videos_result is not UNSET:
            field_dict["ThemeVideosResult"] = theme_videos_result
        if theme_songs_result is not UNSET:
            field_dict["ThemeSongsResult"] = theme_songs_result
        if soundtrack_songs_result is not UNSET:
            field_dict["SoundtrackSongsResult"] = soundtrack_songs_result

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.theme_media_result import ThemeMediaResult

        d = src_dict.copy()
        _theme_videos_result = d.pop("ThemeVideosResult", UNSET)
        theme_videos_result: Union[Unset, ThemeMediaResult]
        if isinstance(_theme_videos_result, Unset):
            theme_videos_result = UNSET
        else:
            theme_videos_result = ThemeMediaResult.from_dict(_theme_videos_result)

        _theme_songs_result = d.pop("ThemeSongsResult", UNSET)
        theme_songs_result: Union[Unset, ThemeMediaResult]
        if isinstance(_theme_songs_result, Unset):
            theme_songs_result = UNSET
        else:
            theme_songs_result = ThemeMediaResult.from_dict(_theme_songs_result)

        _soundtrack_songs_result = d.pop("SoundtrackSongsResult", UNSET)
        soundtrack_songs_result: Union[Unset, ThemeMediaResult]
        if isinstance(_soundtrack_songs_result, Unset):
            soundtrack_songs_result = UNSET
        else:
            soundtrack_songs_result = ThemeMediaResult.from_dict(_soundtrack_songs_result)

        all_theme_media_result = cls(
            theme_videos_result=theme_videos_result,
            theme_songs_result=theme_songs_result,
            soundtrack_songs_result=soundtrack_songs_result,
        )

        all_theme_media_result.additional_properties = d
        return all_theme_media_result

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
