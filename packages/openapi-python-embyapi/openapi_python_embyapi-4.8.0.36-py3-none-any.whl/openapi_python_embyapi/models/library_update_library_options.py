from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.configuration_library_options import ConfigurationLibraryOptions


T = TypeVar("T", bound="LibraryUpdateLibraryOptions")


@attr.s(auto_attribs=True)
class LibraryUpdateLibraryOptions:
    """
    Attributes:
        id (Union[Unset, str]):
        library_options (Union[Unset, ConfigurationLibraryOptions]):
    """

    id: Union[Unset, str] = UNSET
    library_options: Union[Unset, "ConfigurationLibraryOptions"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        library_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.library_options, Unset):
            library_options = self.library_options.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if library_options is not UNSET:
            field_dict["LibraryOptions"] = library_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.configuration_library_options import ConfigurationLibraryOptions

        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        _library_options = d.pop("LibraryOptions", UNSET)
        library_options: Union[Unset, ConfigurationLibraryOptions]
        if isinstance(_library_options, Unset):
            library_options = UNSET
        else:
            library_options = ConfigurationLibraryOptions.from_dict(_library_options)

        library_update_library_options = cls(
            id=id,
            library_options=library_options,
        )

        library_update_library_options.additional_properties = d
        return library_update_library_options

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
