from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.library_sub_folder import LibrarySubFolder


T = TypeVar("T", bound="LibraryMediaFolder")


@attr.s(auto_attribs=True)
class LibraryMediaFolder:
    """
    Attributes:
        name (Union[Unset, str]):
        id (Union[Unset, str]):
        guid (Union[Unset, str]):
        sub_folders (Union[Unset, List['LibrarySubFolder']]):
        is_user_access_configurable (Union[Unset, bool]):
    """

    name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    guid: Union[Unset, str] = UNSET
    sub_folders: Union[Unset, List["LibrarySubFolder"]] = UNSET
    is_user_access_configurable: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        guid = self.guid
        sub_folders: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sub_folders, Unset):
            sub_folders = []
            for sub_folders_item_data in self.sub_folders:
                sub_folders_item = sub_folders_item_data.to_dict()

                sub_folders.append(sub_folders_item)

        is_user_access_configurable = self.is_user_access_configurable

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if id is not UNSET:
            field_dict["Id"] = id
        if guid is not UNSET:
            field_dict["Guid"] = guid
        if sub_folders is not UNSET:
            field_dict["SubFolders"] = sub_folders
        if is_user_access_configurable is not UNSET:
            field_dict["IsUserAccessConfigurable"] = is_user_access_configurable

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.library_sub_folder import LibrarySubFolder

        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        id = d.pop("Id", UNSET)

        guid = d.pop("Guid", UNSET)

        sub_folders = []
        _sub_folders = d.pop("SubFolders", UNSET)
        for sub_folders_item_data in _sub_folders or []:
            sub_folders_item = LibrarySubFolder.from_dict(sub_folders_item_data)

            sub_folders.append(sub_folders_item)

        is_user_access_configurable = d.pop("IsUserAccessConfigurable", UNSET)

        library_media_folder = cls(
            name=name,
            id=id,
            guid=guid,
            sub_folders=sub_folders,
            is_user_access_configurable=is_user_access_configurable,
        )

        library_media_folder.additional_properties = d
        return library_media_folder

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
