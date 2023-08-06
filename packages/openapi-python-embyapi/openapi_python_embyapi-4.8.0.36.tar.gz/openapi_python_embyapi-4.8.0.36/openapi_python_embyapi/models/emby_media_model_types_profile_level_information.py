from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.emby_media_model_types_level_information import EmbyMediaModelTypesLevelInformation
    from ..models.emby_media_model_types_profile_information import EmbyMediaModelTypesProfileInformation


T = TypeVar("T", bound="EmbyMediaModelTypesProfileLevelInformation")


@attr.s(auto_attribs=True)
class EmbyMediaModelTypesProfileLevelInformation:
    """
    Attributes:
        profile (Union[Unset, EmbyMediaModelTypesProfileInformation]):
        level (Union[Unset, EmbyMediaModelTypesLevelInformation]):
    """

    profile: Union[Unset, "EmbyMediaModelTypesProfileInformation"] = UNSET
    level: Union[Unset, "EmbyMediaModelTypesLevelInformation"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        profile: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict()

        level: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.level, Unset):
            level = self.level.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if profile is not UNSET:
            field_dict["Profile"] = profile
        if level is not UNSET:
            field_dict["Level"] = level

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.emby_media_model_types_level_information import EmbyMediaModelTypesLevelInformation
        from ..models.emby_media_model_types_profile_information import EmbyMediaModelTypesProfileInformation

        d = src_dict.copy()
        _profile = d.pop("Profile", UNSET)
        profile: Union[Unset, EmbyMediaModelTypesProfileInformation]
        if isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = EmbyMediaModelTypesProfileInformation.from_dict(_profile)

        _level = d.pop("Level", UNSET)
        level: Union[Unset, EmbyMediaModelTypesLevelInformation]
        if isinstance(_level, Unset):
            level = UNSET
        else:
            level = EmbyMediaModelTypesLevelInformation.from_dict(_level)

        emby_media_model_types_profile_level_information = cls(
            profile=profile,
            level=level,
        )

        emby_media_model_types_profile_level_information.additional_properties = d
        return emby_media_model_types_profile_level_information

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
