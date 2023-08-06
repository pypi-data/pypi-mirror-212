from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="MediaEncodingCodecsCommonInterfacesICodecDeviceCapabilities")


@attr.s(auto_attribs=True)
class MediaEncodingCodecsCommonInterfacesICodecDeviceCapabilities:
    """
    Attributes:
        supports_hw_upload (Union[Unset, bool]):
        supports_hw_download (Union[Unset, bool]):
        supports_standalone_device_init (Union[Unset, bool]):
        supports_10_bit_processing (Union[Unset, bool]):
        supports_native_tone_mapping (Union[Unset, bool]):
    """

    supports_hw_upload: Union[Unset, bool] = UNSET
    supports_hw_download: Union[Unset, bool] = UNSET
    supports_standalone_device_init: Union[Unset, bool] = UNSET
    supports_10_bit_processing: Union[Unset, bool] = UNSET
    supports_native_tone_mapping: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        supports_hw_upload = self.supports_hw_upload
        supports_hw_download = self.supports_hw_download
        supports_standalone_device_init = self.supports_standalone_device_init
        supports_10_bit_processing = self.supports_10_bit_processing
        supports_native_tone_mapping = self.supports_native_tone_mapping

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if supports_hw_upload is not UNSET:
            field_dict["SupportsHwUpload"] = supports_hw_upload
        if supports_hw_download is not UNSET:
            field_dict["SupportsHwDownload"] = supports_hw_download
        if supports_standalone_device_init is not UNSET:
            field_dict["SupportsStandaloneDeviceInit"] = supports_standalone_device_init
        if supports_10_bit_processing is not UNSET:
            field_dict["Supports10BitProcessing"] = supports_10_bit_processing
        if supports_native_tone_mapping is not UNSET:
            field_dict["SupportsNativeToneMapping"] = supports_native_tone_mapping

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        supports_hw_upload = d.pop("SupportsHwUpload", UNSET)

        supports_hw_download = d.pop("SupportsHwDownload", UNSET)

        supports_standalone_device_init = d.pop("SupportsStandaloneDeviceInit", UNSET)

        supports_10_bit_processing = d.pop("Supports10BitProcessing", UNSET)

        supports_native_tone_mapping = d.pop("SupportsNativeToneMapping", UNSET)

        media_encoding_codecs_common_interfaces_i_codec_device_capabilities = cls(
            supports_hw_upload=supports_hw_upload,
            supports_hw_download=supports_hw_download,
            supports_standalone_device_init=supports_standalone_device_init,
            supports_10_bit_processing=supports_10_bit_processing,
            supports_native_tone_mapping=supports_native_tone_mapping,
        )

        media_encoding_codecs_common_interfaces_i_codec_device_capabilities.additional_properties = d
        return media_encoding_codecs_common_interfaces_i_codec_device_capabilities

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
