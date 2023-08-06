from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.emby_media_model_enums_codec_directions import EmbyMediaModelEnumsCodecDirections
from ..models.emby_media_model_enums_codec_kinds import EmbyMediaModelEnumsCodecKinds
from ..models.emby_media_model_enums_color_formats import EmbyMediaModelEnumsColorFormats
from ..models.emby_media_model_enums_secondary_frameworks import EmbyMediaModelEnumsSecondaryFrameworks
from ..models.emby_media_model_enums_video_media_types import EmbyMediaModelEnumsVideoMediaTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.emby_media_model_types_bit_rate import EmbyMediaModelTypesBitRate
    from ..models.emby_media_model_types_profile_level_information import EmbyMediaModelTypesProfileLevelInformation
    from ..models.media_encoding_codecs_common_interfaces_i_codec_device_info import (
        MediaEncodingCodecsCommonInterfacesICodecDeviceInfo,
    )


T = TypeVar("T", bound="MediaEncodingCodecsVideoCodecsVideoCodecBase")


@attr.s(auto_attribs=True)
class MediaEncodingCodecsVideoCodecsVideoCodecBase:
    """
    Attributes:
        codec_device_info (Union[Unset, MediaEncodingCodecsCommonInterfacesICodecDeviceInfo]):
        codec_kind (Union[Unset, EmbyMediaModelEnumsCodecKinds]):
        media_type_name (Union[Unset, str]):
        video_media_type (Union[Unset, EmbyMediaModelEnumsVideoMediaTypes]):
        min_width (Union[Unset, None, int]):
        max_width (Union[Unset, None, int]):
        min_height (Union[Unset, None, int]):
        max_height (Union[Unset, None, int]):
        width_alignment (Union[Unset, None, int]):
        height_alignment (Union[Unset, None, int]):
        max_bit_rate (Union[Unset, EmbyMediaModelTypesBitRate]):
        supported_color_formats (Union[Unset, List[EmbyMediaModelEnumsColorFormats]]):
        supported_color_format_strings (Union[Unset, List[str]]):
        profile_and_level_information (Union[Unset, List['EmbyMediaModelTypesProfileLevelInformation']]):
        id (Union[Unset, str]):
        direction (Union[Unset, EmbyMediaModelEnumsCodecDirections]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        framework_codec (Union[Unset, str]):
        is_hardware_codec (Union[Unset, bool]):
        secondary_framework (Union[Unset, EmbyMediaModelEnumsSecondaryFrameworks]):
        secondary_framework_codec (Union[Unset, str]):
        max_instance_count (Union[Unset, None, int]):
        is_enabled_by_default (Union[Unset, bool]):
        default_priority (Union[Unset, int]):
    """

    codec_device_info: Union[Unset, "MediaEncodingCodecsCommonInterfacesICodecDeviceInfo"] = UNSET
    codec_kind: Union[Unset, EmbyMediaModelEnumsCodecKinds] = UNSET
    media_type_name: Union[Unset, str] = UNSET
    video_media_type: Union[Unset, EmbyMediaModelEnumsVideoMediaTypes] = UNSET
    min_width: Union[Unset, None, int] = UNSET
    max_width: Union[Unset, None, int] = UNSET
    min_height: Union[Unset, None, int] = UNSET
    max_height: Union[Unset, None, int] = UNSET
    width_alignment: Union[Unset, None, int] = UNSET
    height_alignment: Union[Unset, None, int] = UNSET
    max_bit_rate: Union[Unset, "EmbyMediaModelTypesBitRate"] = UNSET
    supported_color_formats: Union[Unset, List[EmbyMediaModelEnumsColorFormats]] = UNSET
    supported_color_format_strings: Union[Unset, List[str]] = UNSET
    profile_and_level_information: Union[Unset, List["EmbyMediaModelTypesProfileLevelInformation"]] = UNSET
    id: Union[Unset, str] = UNSET
    direction: Union[Unset, EmbyMediaModelEnumsCodecDirections] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    framework_codec: Union[Unset, str] = UNSET
    is_hardware_codec: Union[Unset, bool] = UNSET
    secondary_framework: Union[Unset, EmbyMediaModelEnumsSecondaryFrameworks] = UNSET
    secondary_framework_codec: Union[Unset, str] = UNSET
    max_instance_count: Union[Unset, None, int] = UNSET
    is_enabled_by_default: Union[Unset, bool] = UNSET
    default_priority: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        codec_device_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.codec_device_info, Unset):
            codec_device_info = self.codec_device_info.to_dict()

        codec_kind: Union[Unset, str] = UNSET
        if not isinstance(self.codec_kind, Unset):
            codec_kind = self.codec_kind.value

        media_type_name = self.media_type_name
        video_media_type: Union[Unset, str] = UNSET
        if not isinstance(self.video_media_type, Unset):
            video_media_type = self.video_media_type.value

        min_width = self.min_width
        max_width = self.max_width
        min_height = self.min_height
        max_height = self.max_height
        width_alignment = self.width_alignment
        height_alignment = self.height_alignment
        max_bit_rate: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.max_bit_rate, Unset):
            max_bit_rate = self.max_bit_rate.to_dict()

        supported_color_formats: Union[Unset, List[str]] = UNSET
        if not isinstance(self.supported_color_formats, Unset):
            supported_color_formats = []
            for supported_color_formats_item_data in self.supported_color_formats:
                supported_color_formats_item = supported_color_formats_item_data.value

                supported_color_formats.append(supported_color_formats_item)

        supported_color_format_strings: Union[Unset, List[str]] = UNSET
        if not isinstance(self.supported_color_format_strings, Unset):
            supported_color_format_strings = self.supported_color_format_strings

        profile_and_level_information: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.profile_and_level_information, Unset):
            profile_and_level_information = []
            for profile_and_level_information_item_data in self.profile_and_level_information:
                profile_and_level_information_item = profile_and_level_information_item_data.to_dict()

                profile_and_level_information.append(profile_and_level_information_item)

        id = self.id
        direction: Union[Unset, str] = UNSET
        if not isinstance(self.direction, Unset):
            direction = self.direction.value

        name = self.name
        description = self.description
        framework_codec = self.framework_codec
        is_hardware_codec = self.is_hardware_codec
        secondary_framework: Union[Unset, str] = UNSET
        if not isinstance(self.secondary_framework, Unset):
            secondary_framework = self.secondary_framework.value

        secondary_framework_codec = self.secondary_framework_codec
        max_instance_count = self.max_instance_count
        is_enabled_by_default = self.is_enabled_by_default
        default_priority = self.default_priority

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if codec_device_info is not UNSET:
            field_dict["CodecDeviceInfo"] = codec_device_info
        if codec_kind is not UNSET:
            field_dict["CodecKind"] = codec_kind
        if media_type_name is not UNSET:
            field_dict["MediaTypeName"] = media_type_name
        if video_media_type is not UNSET:
            field_dict["VideoMediaType"] = video_media_type
        if min_width is not UNSET:
            field_dict["MinWidth"] = min_width
        if max_width is not UNSET:
            field_dict["MaxWidth"] = max_width
        if min_height is not UNSET:
            field_dict["MinHeight"] = min_height
        if max_height is not UNSET:
            field_dict["MaxHeight"] = max_height
        if width_alignment is not UNSET:
            field_dict["WidthAlignment"] = width_alignment
        if height_alignment is not UNSET:
            field_dict["HeightAlignment"] = height_alignment
        if max_bit_rate is not UNSET:
            field_dict["MaxBitRate"] = max_bit_rate
        if supported_color_formats is not UNSET:
            field_dict["SupportedColorFormats"] = supported_color_formats
        if supported_color_format_strings is not UNSET:
            field_dict["SupportedColorFormatStrings"] = supported_color_format_strings
        if profile_and_level_information is not UNSET:
            field_dict["ProfileAndLevelInformation"] = profile_and_level_information
        if id is not UNSET:
            field_dict["Id"] = id
        if direction is not UNSET:
            field_dict["Direction"] = direction
        if name is not UNSET:
            field_dict["Name"] = name
        if description is not UNSET:
            field_dict["Description"] = description
        if framework_codec is not UNSET:
            field_dict["FrameworkCodec"] = framework_codec
        if is_hardware_codec is not UNSET:
            field_dict["IsHardwareCodec"] = is_hardware_codec
        if secondary_framework is not UNSET:
            field_dict["SecondaryFramework"] = secondary_framework
        if secondary_framework_codec is not UNSET:
            field_dict["SecondaryFrameworkCodec"] = secondary_framework_codec
        if max_instance_count is not UNSET:
            field_dict["MaxInstanceCount"] = max_instance_count
        if is_enabled_by_default is not UNSET:
            field_dict["IsEnabledByDefault"] = is_enabled_by_default
        if default_priority is not UNSET:
            field_dict["DefaultPriority"] = default_priority

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.emby_media_model_types_bit_rate import EmbyMediaModelTypesBitRate
        from ..models.emby_media_model_types_profile_level_information import EmbyMediaModelTypesProfileLevelInformation
        from ..models.media_encoding_codecs_common_interfaces_i_codec_device_info import (
            MediaEncodingCodecsCommonInterfacesICodecDeviceInfo,
        )

        d = src_dict.copy()
        _codec_device_info = d.pop("CodecDeviceInfo", UNSET)
        codec_device_info: Union[Unset, MediaEncodingCodecsCommonInterfacesICodecDeviceInfo]
        if isinstance(_codec_device_info, Unset):
            codec_device_info = UNSET
        else:
            codec_device_info = MediaEncodingCodecsCommonInterfacesICodecDeviceInfo.from_dict(_codec_device_info)

        _codec_kind = d.pop("CodecKind", UNSET)
        codec_kind: Union[Unset, EmbyMediaModelEnumsCodecKinds]
        if isinstance(_codec_kind, Unset):
            codec_kind = UNSET
        else:
            codec_kind = EmbyMediaModelEnumsCodecKinds(_codec_kind)

        media_type_name = d.pop("MediaTypeName", UNSET)

        _video_media_type = d.pop("VideoMediaType", UNSET)
        video_media_type: Union[Unset, EmbyMediaModelEnumsVideoMediaTypes]
        if isinstance(_video_media_type, Unset):
            video_media_type = UNSET
        else:
            video_media_type = EmbyMediaModelEnumsVideoMediaTypes(_video_media_type)

        min_width = d.pop("MinWidth", UNSET)

        max_width = d.pop("MaxWidth", UNSET)

        min_height = d.pop("MinHeight", UNSET)

        max_height = d.pop("MaxHeight", UNSET)

        width_alignment = d.pop("WidthAlignment", UNSET)

        height_alignment = d.pop("HeightAlignment", UNSET)

        _max_bit_rate = d.pop("MaxBitRate", UNSET)
        max_bit_rate: Union[Unset, EmbyMediaModelTypesBitRate]
        if isinstance(_max_bit_rate, Unset):
            max_bit_rate = UNSET
        else:
            max_bit_rate = EmbyMediaModelTypesBitRate.from_dict(_max_bit_rate)

        supported_color_formats = []
        _supported_color_formats = d.pop("SupportedColorFormats", UNSET)
        for supported_color_formats_item_data in _supported_color_formats or []:
            supported_color_formats_item = EmbyMediaModelEnumsColorFormats(supported_color_formats_item_data)

            supported_color_formats.append(supported_color_formats_item)

        supported_color_format_strings = cast(List[str], d.pop("SupportedColorFormatStrings", UNSET))

        profile_and_level_information = []
        _profile_and_level_information = d.pop("ProfileAndLevelInformation", UNSET)
        for profile_and_level_information_item_data in _profile_and_level_information or []:
            profile_and_level_information_item = EmbyMediaModelTypesProfileLevelInformation.from_dict(
                profile_and_level_information_item_data
            )

            profile_and_level_information.append(profile_and_level_information_item)

        id = d.pop("Id", UNSET)

        _direction = d.pop("Direction", UNSET)
        direction: Union[Unset, EmbyMediaModelEnumsCodecDirections]
        if isinstance(_direction, Unset):
            direction = UNSET
        else:
            direction = EmbyMediaModelEnumsCodecDirections(_direction)

        name = d.pop("Name", UNSET)

        description = d.pop("Description", UNSET)

        framework_codec = d.pop("FrameworkCodec", UNSET)

        is_hardware_codec = d.pop("IsHardwareCodec", UNSET)

        _secondary_framework = d.pop("SecondaryFramework", UNSET)
        secondary_framework: Union[Unset, EmbyMediaModelEnumsSecondaryFrameworks]
        if isinstance(_secondary_framework, Unset):
            secondary_framework = UNSET
        else:
            secondary_framework = EmbyMediaModelEnumsSecondaryFrameworks(_secondary_framework)

        secondary_framework_codec = d.pop("SecondaryFrameworkCodec", UNSET)

        max_instance_count = d.pop("MaxInstanceCount", UNSET)

        is_enabled_by_default = d.pop("IsEnabledByDefault", UNSET)

        default_priority = d.pop("DefaultPriority", UNSET)

        media_encoding_codecs_video_codecs_video_codec_base = cls(
            codec_device_info=codec_device_info,
            codec_kind=codec_kind,
            media_type_name=media_type_name,
            video_media_type=video_media_type,
            min_width=min_width,
            max_width=max_width,
            min_height=min_height,
            max_height=max_height,
            width_alignment=width_alignment,
            height_alignment=height_alignment,
            max_bit_rate=max_bit_rate,
            supported_color_formats=supported_color_formats,
            supported_color_format_strings=supported_color_format_strings,
            profile_and_level_information=profile_and_level_information,
            id=id,
            direction=direction,
            name=name,
            description=description,
            framework_codec=framework_codec,
            is_hardware_codec=is_hardware_codec,
            secondary_framework=secondary_framework,
            secondary_framework_codec=secondary_framework_codec,
            max_instance_count=max_instance_count,
            is_enabled_by_default=is_enabled_by_default,
            default_priority=default_priority,
        )

        media_encoding_codecs_video_codecs_video_codec_base.additional_properties = d
        return media_encoding_codecs_video_codecs_video_codec_base

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
