from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.updates_package_version_class import UpdatesPackageVersionClass
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdatesInstallationInfo")


@attr.s(auto_attribs=True)
class UpdatesInstallationInfo:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        assembly_guid (Union[Unset, str]):
        version (Union[Unset, str]):
        update_class (Union[Unset, UpdatesPackageVersionClass]):
        percent_complete (Union[Unset, None, float]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    assembly_guid: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    update_class: Union[Unset, UpdatesPackageVersionClass] = UNSET
    percent_complete: Union[Unset, None, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        assembly_guid = self.assembly_guid
        version = self.version
        update_class: Union[Unset, str] = UNSET
        if not isinstance(self.update_class, Unset):
            update_class = self.update_class.value

        percent_complete = self.percent_complete

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if name is not UNSET:
            field_dict["Name"] = name
        if assembly_guid is not UNSET:
            field_dict["AssemblyGuid"] = assembly_guid
        if version is not UNSET:
            field_dict["Version"] = version
        if update_class is not UNSET:
            field_dict["UpdateClass"] = update_class
        if percent_complete is not UNSET:
            field_dict["PercentComplete"] = percent_complete

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        name = d.pop("Name", UNSET)

        assembly_guid = d.pop("AssemblyGuid", UNSET)

        version = d.pop("Version", UNSET)

        _update_class = d.pop("UpdateClass", UNSET)
        update_class: Union[Unset, UpdatesPackageVersionClass]
        if isinstance(_update_class, Unset):
            update_class = UNSET
        else:
            update_class = UpdatesPackageVersionClass(_update_class)

        percent_complete = d.pop("PercentComplete", UNSET)

        updates_installation_info = cls(
            id=id,
            name=name,
            assembly_guid=assembly_guid,
            version=version,
            update_class=update_class,
            percent_complete=percent_complete,
        )

        updates_installation_info.additional_properties = d
        return updates_installation_info

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
