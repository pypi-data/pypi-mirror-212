from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PluginsPluginInfo")


@attr.s(auto_attribs=True)
class PluginsPluginInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        version (Union[Unset, str]):
        configuration_file_name (Union[Unset, str]):
        description (Union[Unset, str]):
        id (Union[Unset, str]):
        image_tag (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    configuration_file_name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    image_tag: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        version = self.version
        configuration_file_name = self.configuration_file_name
        description = self.description
        id = self.id
        image_tag = self.image_tag

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if version is not UNSET:
            field_dict["Version"] = version
        if configuration_file_name is not UNSET:
            field_dict["ConfigurationFileName"] = configuration_file_name
        if description is not UNSET:
            field_dict["Description"] = description
        if id is not UNSET:
            field_dict["Id"] = id
        if image_tag is not UNSET:
            field_dict["ImageTag"] = image_tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        version = d.pop("Version", UNSET)

        configuration_file_name = d.pop("ConfigurationFileName", UNSET)

        description = d.pop("Description", UNSET)

        id = d.pop("Id", UNSET)

        image_tag = d.pop("ImageTag", UNSET)

        plugins_plugin_info = cls(
            name=name,
            version=version,
            configuration_file_name=configuration_file_name,
            description=description,
            id=id,
            image_tag=image_tag,
        )

        plugins_plugin_info.additional_properties = d
        return plugins_plugin_info

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
