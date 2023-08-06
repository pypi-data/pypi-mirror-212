from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.emby_media_model_enums_secondary_frameworks import EmbyMediaModelEnumsSecondaryFrameworks
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.media_encoding_codecs_common_interfaces_i_codec_device_capabilities import (
        MediaEncodingCodecsCommonInterfacesICodecDeviceCapabilities,
    )
    from ..models.version import Version


T = TypeVar("T", bound="MediaEncodingCodecsCommonInterfacesICodecDeviceInfo")


@attr.s(auto_attribs=True)
class MediaEncodingCodecsCommonInterfacesICodecDeviceInfo:
    """
    Attributes:
        capabilities (Union[Unset, MediaEncodingCodecsCommonInterfacesICodecDeviceCapabilities]):
        adapter (Union[Unset, int]):
        name (Union[Unset, str]):
        desription (Union[Unset, str]):
        driver (Union[Unset, str]):
        driver_version (Union[Unset, Version]):
        api_version (Union[Unset, Version]):
        vendor_id (Union[Unset, int]):
        device_id (Union[Unset, int]):
        device_identifier (Union[Unset, str]):
        hardware_context_framework (Union[Unset, EmbyMediaModelEnumsSecondaryFrameworks]):
        dev_path (Union[Unset, str]):
        drm_node (Union[Unset, str]):
        vendor_name (Union[Unset, str]):
        device_name (Union[Unset, str]):
    """

    capabilities: Union[Unset, "MediaEncodingCodecsCommonInterfacesICodecDeviceCapabilities"] = UNSET
    adapter: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    desription: Union[Unset, str] = UNSET
    driver: Union[Unset, str] = UNSET
    driver_version: Union[Unset, "Version"] = UNSET
    api_version: Union[Unset, "Version"] = UNSET
    vendor_id: Union[Unset, int] = UNSET
    device_id: Union[Unset, int] = UNSET
    device_identifier: Union[Unset, str] = UNSET
    hardware_context_framework: Union[Unset, EmbyMediaModelEnumsSecondaryFrameworks] = UNSET
    dev_path: Union[Unset, str] = UNSET
    drm_node: Union[Unset, str] = UNSET
    vendor_name: Union[Unset, str] = UNSET
    device_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        capabilities: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities.to_dict()

        adapter = self.adapter
        name = self.name
        desription = self.desription
        driver = self.driver
        driver_version: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.driver_version, Unset):
            driver_version = self.driver_version.to_dict()

        api_version: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.api_version, Unset):
            api_version = self.api_version.to_dict()

        vendor_id = self.vendor_id
        device_id = self.device_id
        device_identifier = self.device_identifier
        hardware_context_framework: Union[Unset, str] = UNSET
        if not isinstance(self.hardware_context_framework, Unset):
            hardware_context_framework = self.hardware_context_framework.value

        dev_path = self.dev_path
        drm_node = self.drm_node
        vendor_name = self.vendor_name
        device_name = self.device_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if capabilities is not UNSET:
            field_dict["Capabilities"] = capabilities
        if adapter is not UNSET:
            field_dict["Adapter"] = adapter
        if name is not UNSET:
            field_dict["Name"] = name
        if desription is not UNSET:
            field_dict["Desription"] = desription
        if driver is not UNSET:
            field_dict["Driver"] = driver
        if driver_version is not UNSET:
            field_dict["DriverVersion"] = driver_version
        if api_version is not UNSET:
            field_dict["ApiVersion"] = api_version
        if vendor_id is not UNSET:
            field_dict["VendorId"] = vendor_id
        if device_id is not UNSET:
            field_dict["DeviceId"] = device_id
        if device_identifier is not UNSET:
            field_dict["DeviceIdentifier"] = device_identifier
        if hardware_context_framework is not UNSET:
            field_dict["HardwareContextFramework"] = hardware_context_framework
        if dev_path is not UNSET:
            field_dict["DevPath"] = dev_path
        if drm_node is not UNSET:
            field_dict["DrmNode"] = drm_node
        if vendor_name is not UNSET:
            field_dict["VendorName"] = vendor_name
        if device_name is not UNSET:
            field_dict["DeviceName"] = device_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.media_encoding_codecs_common_interfaces_i_codec_device_capabilities import (
            MediaEncodingCodecsCommonInterfacesICodecDeviceCapabilities,
        )
        from ..models.version import Version

        d = src_dict.copy()
        _capabilities = d.pop("Capabilities", UNSET)
        capabilities: Union[Unset, MediaEncodingCodecsCommonInterfacesICodecDeviceCapabilities]
        if isinstance(_capabilities, Unset):
            capabilities = UNSET
        else:
            capabilities = MediaEncodingCodecsCommonInterfacesICodecDeviceCapabilities.from_dict(_capabilities)

        adapter = d.pop("Adapter", UNSET)

        name = d.pop("Name", UNSET)

        desription = d.pop("Desription", UNSET)

        driver = d.pop("Driver", UNSET)

        _driver_version = d.pop("DriverVersion", UNSET)
        driver_version: Union[Unset, Version]
        if isinstance(_driver_version, Unset):
            driver_version = UNSET
        else:
            driver_version = Version.from_dict(_driver_version)

        _api_version = d.pop("ApiVersion", UNSET)
        api_version: Union[Unset, Version]
        if isinstance(_api_version, Unset):
            api_version = UNSET
        else:
            api_version = Version.from_dict(_api_version)

        vendor_id = d.pop("VendorId", UNSET)

        device_id = d.pop("DeviceId", UNSET)

        device_identifier = d.pop("DeviceIdentifier", UNSET)

        _hardware_context_framework = d.pop("HardwareContextFramework", UNSET)
        hardware_context_framework: Union[Unset, EmbyMediaModelEnumsSecondaryFrameworks]
        if isinstance(_hardware_context_framework, Unset):
            hardware_context_framework = UNSET
        else:
            hardware_context_framework = EmbyMediaModelEnumsSecondaryFrameworks(_hardware_context_framework)

        dev_path = d.pop("DevPath", UNSET)

        drm_node = d.pop("DrmNode", UNSET)

        vendor_name = d.pop("VendorName", UNSET)

        device_name = d.pop("DeviceName", UNSET)

        media_encoding_codecs_common_interfaces_i_codec_device_info = cls(
            capabilities=capabilities,
            adapter=adapter,
            name=name,
            desription=desription,
            driver=driver,
            driver_version=driver_version,
            api_version=api_version,
            vendor_id=vendor_id,
            device_id=device_id,
            device_identifier=device_identifier,
            hardware_context_framework=hardware_context_framework,
            dev_path=dev_path,
            drm_node=drm_node,
            vendor_name=vendor_name,
            device_name=device_name,
        )

        media_encoding_codecs_common_interfaces_i_codec_device_info.additional_properties = d
        return media_encoding_codecs_common_interfaces_i_codec_device_info

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
