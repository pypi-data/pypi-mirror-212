from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.transcoding_vp_step_types import TranscodingVpStepTypes
from ..types import UNSET, Unset

T = TypeVar("T", bound="TranscodingVpStepInfo")


@attr.s(auto_attribs=True)
class TranscodingVpStepInfo:
    """
    Attributes:
        step_type (Union[Unset, TranscodingVpStepTypes]):
        step_type_name (Union[Unset, str]):
        hardware_context_name (Union[Unset, str]):
        is_hardware_context (Union[Unset, bool]):
        name (Union[Unset, str]):
        short (Union[Unset, str]):
        ffmpeg_name (Union[Unset, str]):
        ffmpeg_description (Union[Unset, str]):
        ffmpeg_options (Union[Unset, str]):
        param (Union[Unset, str]):
        param_short (Union[Unset, str]):
    """

    step_type: Union[Unset, TranscodingVpStepTypes] = UNSET
    step_type_name: Union[Unset, str] = UNSET
    hardware_context_name: Union[Unset, str] = UNSET
    is_hardware_context: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    short: Union[Unset, str] = UNSET
    ffmpeg_name: Union[Unset, str] = UNSET
    ffmpeg_description: Union[Unset, str] = UNSET
    ffmpeg_options: Union[Unset, str] = UNSET
    param: Union[Unset, str] = UNSET
    param_short: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        step_type: Union[Unset, str] = UNSET
        if not isinstance(self.step_type, Unset):
            step_type = self.step_type.value

        step_type_name = self.step_type_name
        hardware_context_name = self.hardware_context_name
        is_hardware_context = self.is_hardware_context
        name = self.name
        short = self.short
        ffmpeg_name = self.ffmpeg_name
        ffmpeg_description = self.ffmpeg_description
        ffmpeg_options = self.ffmpeg_options
        param = self.param
        param_short = self.param_short

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if step_type is not UNSET:
            field_dict["StepType"] = step_type
        if step_type_name is not UNSET:
            field_dict["StepTypeName"] = step_type_name
        if hardware_context_name is not UNSET:
            field_dict["HardwareContextName"] = hardware_context_name
        if is_hardware_context is not UNSET:
            field_dict["IsHardwareContext"] = is_hardware_context
        if name is not UNSET:
            field_dict["Name"] = name
        if short is not UNSET:
            field_dict["Short"] = short
        if ffmpeg_name is not UNSET:
            field_dict["FfmpegName"] = ffmpeg_name
        if ffmpeg_description is not UNSET:
            field_dict["FfmpegDescription"] = ffmpeg_description
        if ffmpeg_options is not UNSET:
            field_dict["FfmpegOptions"] = ffmpeg_options
        if param is not UNSET:
            field_dict["Param"] = param
        if param_short is not UNSET:
            field_dict["ParamShort"] = param_short

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _step_type = d.pop("StepType", UNSET)
        step_type: Union[Unset, TranscodingVpStepTypes]
        if isinstance(_step_type, Unset):
            step_type = UNSET
        else:
            step_type = TranscodingVpStepTypes(_step_type)

        step_type_name = d.pop("StepTypeName", UNSET)

        hardware_context_name = d.pop("HardwareContextName", UNSET)

        is_hardware_context = d.pop("IsHardwareContext", UNSET)

        name = d.pop("Name", UNSET)

        short = d.pop("Short", UNSET)

        ffmpeg_name = d.pop("FfmpegName", UNSET)

        ffmpeg_description = d.pop("FfmpegDescription", UNSET)

        ffmpeg_options = d.pop("FfmpegOptions", UNSET)

        param = d.pop("Param", UNSET)

        param_short = d.pop("ParamShort", UNSET)

        transcoding_vp_step_info = cls(
            step_type=step_type,
            step_type_name=step_type_name,
            hardware_context_name=hardware_context_name,
            is_hardware_context=is_hardware_context,
            name=name,
            short=short,
            ffmpeg_name=ffmpeg_name,
            ffmpeg_description=ffmpeg_description,
            ffmpeg_options=ffmpeg_options,
            param=param,
            param_short=param_short,
        )

        transcoding_vp_step_info.additional_properties = d
        return transcoding_vp_step_info

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
