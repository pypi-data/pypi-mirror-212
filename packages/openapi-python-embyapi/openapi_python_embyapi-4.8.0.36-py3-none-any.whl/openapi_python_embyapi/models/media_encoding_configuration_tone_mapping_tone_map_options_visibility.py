from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.operating_system import OperatingSystem
from ..types import UNSET, Unset

T = TypeVar("T", bound="MediaEncodingConfigurationToneMappingToneMapOptionsVisibility")


@attr.s(auto_attribs=True)
class MediaEncodingConfigurationToneMappingToneMapOptionsVisibility:
    """
    Attributes:
        show_advanced (Union[Unset, bool]):
        is_software_tone_mapping_available (Union[Unset, bool]):
        is_any_hardware_tone_mapping_available (Union[Unset, bool]):
        show_nvidia_options (Union[Unset, bool]):
        show_quick_sync_options (Union[Unset, bool]):
        show_vaapi_options (Union[Unset, bool]):
        is_open_cl_available (Union[Unset, bool]):
        is_open_cl_super_t_available (Union[Unset, bool]):
        is_vaapi_native_available (Union[Unset, bool]):
        is_quick_sync_native_available (Union[Unset, bool]):
        operating_system (Union[Unset, OperatingSystem]):
    """

    show_advanced: Union[Unset, bool] = UNSET
    is_software_tone_mapping_available: Union[Unset, bool] = UNSET
    is_any_hardware_tone_mapping_available: Union[Unset, bool] = UNSET
    show_nvidia_options: Union[Unset, bool] = UNSET
    show_quick_sync_options: Union[Unset, bool] = UNSET
    show_vaapi_options: Union[Unset, bool] = UNSET
    is_open_cl_available: Union[Unset, bool] = UNSET
    is_open_cl_super_t_available: Union[Unset, bool] = UNSET
    is_vaapi_native_available: Union[Unset, bool] = UNSET
    is_quick_sync_native_available: Union[Unset, bool] = UNSET
    operating_system: Union[Unset, OperatingSystem] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        show_advanced = self.show_advanced
        is_software_tone_mapping_available = self.is_software_tone_mapping_available
        is_any_hardware_tone_mapping_available = self.is_any_hardware_tone_mapping_available
        show_nvidia_options = self.show_nvidia_options
        show_quick_sync_options = self.show_quick_sync_options
        show_vaapi_options = self.show_vaapi_options
        is_open_cl_available = self.is_open_cl_available
        is_open_cl_super_t_available = self.is_open_cl_super_t_available
        is_vaapi_native_available = self.is_vaapi_native_available
        is_quick_sync_native_available = self.is_quick_sync_native_available
        operating_system: Union[Unset, str] = UNSET
        if not isinstance(self.operating_system, Unset):
            operating_system = self.operating_system.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if show_advanced is not UNSET:
            field_dict["ShowAdvanced"] = show_advanced
        if is_software_tone_mapping_available is not UNSET:
            field_dict["IsSoftwareToneMappingAvailable"] = is_software_tone_mapping_available
        if is_any_hardware_tone_mapping_available is not UNSET:
            field_dict["IsAnyHardwareToneMappingAvailable"] = is_any_hardware_tone_mapping_available
        if show_nvidia_options is not UNSET:
            field_dict["ShowNvidiaOptions"] = show_nvidia_options
        if show_quick_sync_options is not UNSET:
            field_dict["ShowQuickSyncOptions"] = show_quick_sync_options
        if show_vaapi_options is not UNSET:
            field_dict["ShowVaapiOptions"] = show_vaapi_options
        if is_open_cl_available is not UNSET:
            field_dict["IsOpenClAvailable"] = is_open_cl_available
        if is_open_cl_super_t_available is not UNSET:
            field_dict["IsOpenClSuperTAvailable"] = is_open_cl_super_t_available
        if is_vaapi_native_available is not UNSET:
            field_dict["IsVaapiNativeAvailable"] = is_vaapi_native_available
        if is_quick_sync_native_available is not UNSET:
            field_dict["IsQuickSyncNativeAvailable"] = is_quick_sync_native_available
        if operating_system is not UNSET:
            field_dict["OperatingSystem"] = operating_system

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        show_advanced = d.pop("ShowAdvanced", UNSET)

        is_software_tone_mapping_available = d.pop("IsSoftwareToneMappingAvailable", UNSET)

        is_any_hardware_tone_mapping_available = d.pop("IsAnyHardwareToneMappingAvailable", UNSET)

        show_nvidia_options = d.pop("ShowNvidiaOptions", UNSET)

        show_quick_sync_options = d.pop("ShowQuickSyncOptions", UNSET)

        show_vaapi_options = d.pop("ShowVaapiOptions", UNSET)

        is_open_cl_available = d.pop("IsOpenClAvailable", UNSET)

        is_open_cl_super_t_available = d.pop("IsOpenClSuperTAvailable", UNSET)

        is_vaapi_native_available = d.pop("IsVaapiNativeAvailable", UNSET)

        is_quick_sync_native_available = d.pop("IsQuickSyncNativeAvailable", UNSET)

        _operating_system = d.pop("OperatingSystem", UNSET)
        operating_system: Union[Unset, OperatingSystem]
        if isinstance(_operating_system, Unset):
            operating_system = UNSET
        else:
            operating_system = OperatingSystem(_operating_system)

        media_encoding_configuration_tone_mapping_tone_map_options_visibility = cls(
            show_advanced=show_advanced,
            is_software_tone_mapping_available=is_software_tone_mapping_available,
            is_any_hardware_tone_mapping_available=is_any_hardware_tone_mapping_available,
            show_nvidia_options=show_nvidia_options,
            show_quick_sync_options=show_quick_sync_options,
            show_vaapi_options=show_vaapi_options,
            is_open_cl_available=is_open_cl_available,
            is_open_cl_super_t_available=is_open_cl_super_t_available,
            is_vaapi_native_available=is_vaapi_native_available,
            is_quick_sync_native_available=is_quick_sync_native_available,
            operating_system=operating_system,
        )

        media_encoding_configuration_tone_mapping_tone_map_options_visibility.additional_properties = d
        return media_encoding_configuration_tone_mapping_tone_map_options_visibility

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
