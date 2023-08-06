from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.configuration_media_path_info import ConfigurationMediaPathInfo


T = TypeVar("T", bound="LibraryUpdateMediaPath")


@attr.s(auto_attribs=True)
class LibraryUpdateMediaPath:
    """
    Attributes:
        id (Union[Unset, str]):
        path_info (Union[Unset, ConfigurationMediaPathInfo]):
    """

    id: Union[Unset, str] = UNSET
    path_info: Union[Unset, "ConfigurationMediaPathInfo"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        path_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.path_info, Unset):
            path_info = self.path_info.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if path_info is not UNSET:
            field_dict["PathInfo"] = path_info

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.configuration_media_path_info import ConfigurationMediaPathInfo

        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        _path_info = d.pop("PathInfo", UNSET)
        path_info: Union[Unset, ConfigurationMediaPathInfo]
        if isinstance(_path_info, Unset):
            path_info = UNSET
        else:
            path_info = ConfigurationMediaPathInfo.from_dict(_path_info)

        library_update_media_path = cls(
            id=id,
            path_info=path_info,
        )

        library_update_media_path.additional_properties = d
        return library_update_media_path

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
