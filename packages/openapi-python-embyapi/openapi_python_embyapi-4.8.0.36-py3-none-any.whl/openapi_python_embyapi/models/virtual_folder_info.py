from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.configuration_library_options import ConfigurationLibraryOptions


T = TypeVar("T", bound="VirtualFolderInfo")


@attr.s(auto_attribs=True)
class VirtualFolderInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        locations (Union[Unset, List[str]]):
        collection_type (Union[Unset, str]):
        library_options (Union[Unset, ConfigurationLibraryOptions]):
        item_id (Union[Unset, str]):
        id (Union[Unset, str]):
        guid (Union[Unset, str]):
        primary_image_item_id (Union[Unset, str]):
        refresh_progress (Union[Unset, None, float]):
        refresh_status (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    locations: Union[Unset, List[str]] = UNSET
    collection_type: Union[Unset, str] = UNSET
    library_options: Union[Unset, "ConfigurationLibraryOptions"] = UNSET
    item_id: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    guid: Union[Unset, str] = UNSET
    primary_image_item_id: Union[Unset, str] = UNSET
    refresh_progress: Union[Unset, None, float] = UNSET
    refresh_status: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        locations: Union[Unset, List[str]] = UNSET
        if not isinstance(self.locations, Unset):
            locations = self.locations

        collection_type = self.collection_type
        library_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.library_options, Unset):
            library_options = self.library_options.to_dict()

        item_id = self.item_id
        id = self.id
        guid = self.guid
        primary_image_item_id = self.primary_image_item_id
        refresh_progress = self.refresh_progress
        refresh_status = self.refresh_status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if locations is not UNSET:
            field_dict["Locations"] = locations
        if collection_type is not UNSET:
            field_dict["CollectionType"] = collection_type
        if library_options is not UNSET:
            field_dict["LibraryOptions"] = library_options
        if item_id is not UNSET:
            field_dict["ItemId"] = item_id
        if id is not UNSET:
            field_dict["Id"] = id
        if guid is not UNSET:
            field_dict["Guid"] = guid
        if primary_image_item_id is not UNSET:
            field_dict["PrimaryImageItemId"] = primary_image_item_id
        if refresh_progress is not UNSET:
            field_dict["RefreshProgress"] = refresh_progress
        if refresh_status is not UNSET:
            field_dict["RefreshStatus"] = refresh_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.configuration_library_options import ConfigurationLibraryOptions

        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        locations = cast(List[str], d.pop("Locations", UNSET))

        collection_type = d.pop("CollectionType", UNSET)

        _library_options = d.pop("LibraryOptions", UNSET)
        library_options: Union[Unset, ConfigurationLibraryOptions]
        if isinstance(_library_options, Unset):
            library_options = UNSET
        else:
            library_options = ConfigurationLibraryOptions.from_dict(_library_options)

        item_id = d.pop("ItemId", UNSET)

        id = d.pop("Id", UNSET)

        guid = d.pop("Guid", UNSET)

        primary_image_item_id = d.pop("PrimaryImageItemId", UNSET)

        refresh_progress = d.pop("RefreshProgress", UNSET)

        refresh_status = d.pop("RefreshStatus", UNSET)

        virtual_folder_info = cls(
            name=name,
            locations=locations,
            collection_type=collection_type,
            library_options=library_options,
            item_id=item_id,
            id=id,
            guid=guid,
            primary_image_item_id=primary_image_item_id,
            refresh_progress=refresh_progress,
            refresh_status=refresh_status,
        )

        virtual_folder_info.additional_properties = d
        return virtual_folder_info

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
