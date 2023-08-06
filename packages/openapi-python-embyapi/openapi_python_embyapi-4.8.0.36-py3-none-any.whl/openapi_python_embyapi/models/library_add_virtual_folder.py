from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.configuration_library_options import ConfigurationLibraryOptions


T = TypeVar("T", bound="LibraryAddVirtualFolder")


@attr.s(auto_attribs=True)
class LibraryAddVirtualFolder:
    """
    Attributes:
        name (Union[Unset, str]):
        collection_type (Union[Unset, str]):
        refresh_library (Union[Unset, bool]):
        paths (Union[Unset, List[str]]):
        library_options (Union[Unset, ConfigurationLibraryOptions]):
    """

    name: Union[Unset, str] = UNSET
    collection_type: Union[Unset, str] = UNSET
    refresh_library: Union[Unset, bool] = UNSET
    paths: Union[Unset, List[str]] = UNSET
    library_options: Union[Unset, "ConfigurationLibraryOptions"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        collection_type = self.collection_type
        refresh_library = self.refresh_library
        paths: Union[Unset, List[str]] = UNSET
        if not isinstance(self.paths, Unset):
            paths = self.paths

        library_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.library_options, Unset):
            library_options = self.library_options.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if collection_type is not UNSET:
            field_dict["CollectionType"] = collection_type
        if refresh_library is not UNSET:
            field_dict["RefreshLibrary"] = refresh_library
        if paths is not UNSET:
            field_dict["Paths"] = paths
        if library_options is not UNSET:
            field_dict["LibraryOptions"] = library_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.configuration_library_options import ConfigurationLibraryOptions

        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        collection_type = d.pop("CollectionType", UNSET)

        refresh_library = d.pop("RefreshLibrary", UNSET)

        paths = cast(List[str], d.pop("Paths", UNSET))

        _library_options = d.pop("LibraryOptions", UNSET)
        library_options: Union[Unset, ConfigurationLibraryOptions]
        if isinstance(_library_options, Unset):
            library_options = UNSET
        else:
            library_options = ConfigurationLibraryOptions.from_dict(_library_options)

        library_add_virtual_folder = cls(
            name=name,
            collection_type=collection_type,
            refresh_library=refresh_library,
            paths=paths,
            library_options=library_options,
        )

        library_add_virtual_folder.additional_properties = d
        return library_add_virtual_folder

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
