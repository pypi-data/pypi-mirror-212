from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.version import Version


T = TypeVar("T", bound="CommonPluginsIPlugin")


@attr.s(auto_attribs=True)
class CommonPluginsIPlugin:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        id (Union[Unset, str]):
        version (Union[Unset, Version]):
        assembly_file_path (Union[Unset, str]):
        data_folder_path (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    version: Union[Unset, "Version"] = UNSET
    assembly_file_path: Union[Unset, str] = UNSET
    data_folder_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        id = self.id
        version: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.version, Unset):
            version = self.version.to_dict()

        assembly_file_path = self.assembly_file_path
        data_folder_path = self.data_folder_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if description is not UNSET:
            field_dict["Description"] = description
        if id is not UNSET:
            field_dict["Id"] = id
        if version is not UNSET:
            field_dict["Version"] = version
        if assembly_file_path is not UNSET:
            field_dict["AssemblyFilePath"] = assembly_file_path
        if data_folder_path is not UNSET:
            field_dict["DataFolderPath"] = data_folder_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.version import Version

        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        description = d.pop("Description", UNSET)

        id = d.pop("Id", UNSET)

        _version = d.pop("Version", UNSET)
        version: Union[Unset, Version]
        if isinstance(_version, Unset):
            version = UNSET
        else:
            version = Version.from_dict(_version)

        assembly_file_path = d.pop("AssemblyFilePath", UNSET)

        data_folder_path = d.pop("DataFolderPath", UNSET)

        common_plugins_i_plugin = cls(
            name=name,
            description=description,
            id=id,
            version=version,
            assembly_file_path=assembly_file_path,
            data_folder_path=data_folder_path,
        )

        common_plugins_i_plugin.additional_properties = d
        return common_plugins_i_plugin

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
