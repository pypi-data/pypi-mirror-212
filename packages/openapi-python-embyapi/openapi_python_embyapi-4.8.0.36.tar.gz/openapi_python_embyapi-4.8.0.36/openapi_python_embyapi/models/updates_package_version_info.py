import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.updates_package_version_class import UpdatesPackageVersionClass
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdatesPackageVersionInfo")


@attr.s(auto_attribs=True)
class UpdatesPackageVersionInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        guid (Union[Unset, str]):
        version_str (Union[Unset, str]):
        classification (Union[Unset, UpdatesPackageVersionClass]):
        description (Union[Unset, str]):
        required_version_str (Union[Unset, str]):
        source_url (Union[Unset, str]):
        checksum (Union[Unset, str]):
        target_filename (Union[Unset, str]):
        info_url (Union[Unset, str]):
        runtimes (Union[Unset, str]):
        timestamp (Union[Unset, None, datetime.datetime]):
    """

    name: Union[Unset, str] = UNSET
    guid: Union[Unset, str] = UNSET
    version_str: Union[Unset, str] = UNSET
    classification: Union[Unset, UpdatesPackageVersionClass] = UNSET
    description: Union[Unset, str] = UNSET
    required_version_str: Union[Unset, str] = UNSET
    source_url: Union[Unset, str] = UNSET
    checksum: Union[Unset, str] = UNSET
    target_filename: Union[Unset, str] = UNSET
    info_url: Union[Unset, str] = UNSET
    runtimes: Union[Unset, str] = UNSET
    timestamp: Union[Unset, None, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        guid = self.guid
        version_str = self.version_str
        classification: Union[Unset, str] = UNSET
        if not isinstance(self.classification, Unset):
            classification = self.classification.value

        description = self.description
        required_version_str = self.required_version_str
        source_url = self.source_url
        checksum = self.checksum
        target_filename = self.target_filename
        info_url = self.info_url
        runtimes = self.runtimes
        timestamp: Union[Unset, None, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat() if self.timestamp else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if guid is not UNSET:
            field_dict["guid"] = guid
        if version_str is not UNSET:
            field_dict["versionStr"] = version_str
        if classification is not UNSET:
            field_dict["classification"] = classification
        if description is not UNSET:
            field_dict["description"] = description
        if required_version_str is not UNSET:
            field_dict["requiredVersionStr"] = required_version_str
        if source_url is not UNSET:
            field_dict["sourceUrl"] = source_url
        if checksum is not UNSET:
            field_dict["checksum"] = checksum
        if target_filename is not UNSET:
            field_dict["targetFilename"] = target_filename
        if info_url is not UNSET:
            field_dict["infoUrl"] = info_url
        if runtimes is not UNSET:
            field_dict["runtimes"] = runtimes
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        guid = d.pop("guid", UNSET)

        version_str = d.pop("versionStr", UNSET)

        _classification = d.pop("classification", UNSET)
        classification: Union[Unset, UpdatesPackageVersionClass]
        if isinstance(_classification, Unset):
            classification = UNSET
        else:
            classification = UpdatesPackageVersionClass(_classification)

        description = d.pop("description", UNSET)

        required_version_str = d.pop("requiredVersionStr", UNSET)

        source_url = d.pop("sourceUrl", UNSET)

        checksum = d.pop("checksum", UNSET)

        target_filename = d.pop("targetFilename", UNSET)

        info_url = d.pop("infoUrl", UNSET)

        runtimes = d.pop("runtimes", UNSET)

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, None, datetime.datetime]
        if _timestamp is None:
            timestamp = None
        elif isinstance(_timestamp, Unset):
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)

        updates_package_version_info = cls(
            name=name,
            guid=guid,
            version_str=version_str,
            classification=classification,
            description=description,
            required_version_str=required_version_str,
            source_url=source_url,
            checksum=checksum,
            target_filename=target_filename,
            info_url=info_url,
            runtimes=runtimes,
            timestamp=timestamp,
        )

        updates_package_version_info.additional_properties = d
        return updates_package_version_info

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
