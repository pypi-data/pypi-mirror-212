from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.transcode_reason import TranscodeReason
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.process_run_metrics_process_statistics import ProcessRunMetricsProcessStatistics
    from ..models.transcoding_vp_step_info import TranscodingVpStepInfo
    from ..models.tuple_double_double import TupleDoubleDouble


T = TypeVar("T", bound="TranscodingInfo")


@attr.s(auto_attribs=True)
class TranscodingInfo:
    """
    Attributes:
        audio_codec (Union[Unset, str]):
        video_codec (Union[Unset, str]):
        sub_protocol (Union[Unset, str]):
        container (Union[Unset, str]):
        is_video_direct (Union[Unset, bool]):
        is_audio_direct (Union[Unset, bool]):
        bitrate (Union[Unset, None, int]):
        audio_bitrate (Union[Unset, None, int]):
        video_bitrate (Union[Unset, None, int]):
        framerate (Union[Unset, None, float]):
        completion_percentage (Union[Unset, None, float]):
        transcoding_position_ticks (Union[Unset, None, float]):
        transcoding_start_position_ticks (Union[Unset, None, float]):
        width (Union[Unset, None, int]):
        height (Union[Unset, None, int]):
        audio_channels (Union[Unset, None, int]):
        transcode_reasons (Union[Unset, List[TranscodeReason]]):
        current_cpu_usage (Union[Unset, None, float]):
        average_cpu_usage (Union[Unset, None, float]):
        cpu_history (Union[Unset, List['TupleDoubleDouble']]):
        process_statistics (Union[Unset, ProcessRunMetricsProcessStatistics]):
        current_throttle (Union[Unset, None, int]):
        video_decoder (Union[Unset, str]):
        video_decoder_is_hardware (Union[Unset, bool]):
        video_decoder_media_type (Union[Unset, str]):
        video_decoder_hw_accel (Union[Unset, str]):
        video_encoder (Union[Unset, str]):
        video_encoder_is_hardware (Union[Unset, bool]):
        video_encoder_media_type (Union[Unset, str]):
        video_encoder_hw_accel (Union[Unset, str]):
        video_pipeline_info (Union[Unset, List['TranscodingVpStepInfo']]):
        subtitle_pipeline_infos (Union[Unset, List[List['TranscodingVpStepInfo']]]):
    """

    audio_codec: Union[Unset, str] = UNSET
    video_codec: Union[Unset, str] = UNSET
    sub_protocol: Union[Unset, str] = UNSET
    container: Union[Unset, str] = UNSET
    is_video_direct: Union[Unset, bool] = UNSET
    is_audio_direct: Union[Unset, bool] = UNSET
    bitrate: Union[Unset, None, int] = UNSET
    audio_bitrate: Union[Unset, None, int] = UNSET
    video_bitrate: Union[Unset, None, int] = UNSET
    framerate: Union[Unset, None, float] = UNSET
    completion_percentage: Union[Unset, None, float] = UNSET
    transcoding_position_ticks: Union[Unset, None, float] = UNSET
    transcoding_start_position_ticks: Union[Unset, None, float] = UNSET
    width: Union[Unset, None, int] = UNSET
    height: Union[Unset, None, int] = UNSET
    audio_channels: Union[Unset, None, int] = UNSET
    transcode_reasons: Union[Unset, List[TranscodeReason]] = UNSET
    current_cpu_usage: Union[Unset, None, float] = UNSET
    average_cpu_usage: Union[Unset, None, float] = UNSET
    cpu_history: Union[Unset, List["TupleDoubleDouble"]] = UNSET
    process_statistics: Union[Unset, "ProcessRunMetricsProcessStatistics"] = UNSET
    current_throttle: Union[Unset, None, int] = UNSET
    video_decoder: Union[Unset, str] = UNSET
    video_decoder_is_hardware: Union[Unset, bool] = UNSET
    video_decoder_media_type: Union[Unset, str] = UNSET
    video_decoder_hw_accel: Union[Unset, str] = UNSET
    video_encoder: Union[Unset, str] = UNSET
    video_encoder_is_hardware: Union[Unset, bool] = UNSET
    video_encoder_media_type: Union[Unset, str] = UNSET
    video_encoder_hw_accel: Union[Unset, str] = UNSET
    video_pipeline_info: Union[Unset, List["TranscodingVpStepInfo"]] = UNSET
    subtitle_pipeline_infos: Union[Unset, List[List["TranscodingVpStepInfo"]]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        audio_codec = self.audio_codec
        video_codec = self.video_codec
        sub_protocol = self.sub_protocol
        container = self.container
        is_video_direct = self.is_video_direct
        is_audio_direct = self.is_audio_direct
        bitrate = self.bitrate
        audio_bitrate = self.audio_bitrate
        video_bitrate = self.video_bitrate
        framerate = self.framerate
        completion_percentage = self.completion_percentage
        transcoding_position_ticks = self.transcoding_position_ticks
        transcoding_start_position_ticks = self.transcoding_start_position_ticks
        width = self.width
        height = self.height
        audio_channels = self.audio_channels
        transcode_reasons: Union[Unset, List[str]] = UNSET
        if not isinstance(self.transcode_reasons, Unset):
            transcode_reasons = []
            for transcode_reasons_item_data in self.transcode_reasons:
                transcode_reasons_item = transcode_reasons_item_data.value

                transcode_reasons.append(transcode_reasons_item)

        current_cpu_usage = self.current_cpu_usage
        average_cpu_usage = self.average_cpu_usage
        cpu_history: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.cpu_history, Unset):
            cpu_history = []
            for cpu_history_item_data in self.cpu_history:
                cpu_history_item = cpu_history_item_data.to_dict()

                cpu_history.append(cpu_history_item)

        process_statistics: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.process_statistics, Unset):
            process_statistics = self.process_statistics.to_dict()

        current_throttle = self.current_throttle
        video_decoder = self.video_decoder
        video_decoder_is_hardware = self.video_decoder_is_hardware
        video_decoder_media_type = self.video_decoder_media_type
        video_decoder_hw_accel = self.video_decoder_hw_accel
        video_encoder = self.video_encoder
        video_encoder_is_hardware = self.video_encoder_is_hardware
        video_encoder_media_type = self.video_encoder_media_type
        video_encoder_hw_accel = self.video_encoder_hw_accel
        video_pipeline_info: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.video_pipeline_info, Unset):
            video_pipeline_info = []
            for video_pipeline_info_item_data in self.video_pipeline_info:
                video_pipeline_info_item = video_pipeline_info_item_data.to_dict()

                video_pipeline_info.append(video_pipeline_info_item)

        subtitle_pipeline_infos: Union[Unset, List[List[Dict[str, Any]]]] = UNSET
        if not isinstance(self.subtitle_pipeline_infos, Unset):
            subtitle_pipeline_infos = []
            for subtitle_pipeline_infos_item_data in self.subtitle_pipeline_infos:
                subtitle_pipeline_infos_item = []
                for subtitle_pipeline_infos_item_item_data in subtitle_pipeline_infos_item_data:
                    subtitle_pipeline_infos_item_item = subtitle_pipeline_infos_item_item_data.to_dict()

                    subtitle_pipeline_infos_item.append(subtitle_pipeline_infos_item_item)

                subtitle_pipeline_infos.append(subtitle_pipeline_infos_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if audio_codec is not UNSET:
            field_dict["AudioCodec"] = audio_codec
        if video_codec is not UNSET:
            field_dict["VideoCodec"] = video_codec
        if sub_protocol is not UNSET:
            field_dict["SubProtocol"] = sub_protocol
        if container is not UNSET:
            field_dict["Container"] = container
        if is_video_direct is not UNSET:
            field_dict["IsVideoDirect"] = is_video_direct
        if is_audio_direct is not UNSET:
            field_dict["IsAudioDirect"] = is_audio_direct
        if bitrate is not UNSET:
            field_dict["Bitrate"] = bitrate
        if audio_bitrate is not UNSET:
            field_dict["AudioBitrate"] = audio_bitrate
        if video_bitrate is not UNSET:
            field_dict["VideoBitrate"] = video_bitrate
        if framerate is not UNSET:
            field_dict["Framerate"] = framerate
        if completion_percentage is not UNSET:
            field_dict["CompletionPercentage"] = completion_percentage
        if transcoding_position_ticks is not UNSET:
            field_dict["TranscodingPositionTicks"] = transcoding_position_ticks
        if transcoding_start_position_ticks is not UNSET:
            field_dict["TranscodingStartPositionTicks"] = transcoding_start_position_ticks
        if width is not UNSET:
            field_dict["Width"] = width
        if height is not UNSET:
            field_dict["Height"] = height
        if audio_channels is not UNSET:
            field_dict["AudioChannels"] = audio_channels
        if transcode_reasons is not UNSET:
            field_dict["TranscodeReasons"] = transcode_reasons
        if current_cpu_usage is not UNSET:
            field_dict["CurrentCpuUsage"] = current_cpu_usage
        if average_cpu_usage is not UNSET:
            field_dict["AverageCpuUsage"] = average_cpu_usage
        if cpu_history is not UNSET:
            field_dict["CpuHistory"] = cpu_history
        if process_statistics is not UNSET:
            field_dict["ProcessStatistics"] = process_statistics
        if current_throttle is not UNSET:
            field_dict["CurrentThrottle"] = current_throttle
        if video_decoder is not UNSET:
            field_dict["VideoDecoder"] = video_decoder
        if video_decoder_is_hardware is not UNSET:
            field_dict["VideoDecoderIsHardware"] = video_decoder_is_hardware
        if video_decoder_media_type is not UNSET:
            field_dict["VideoDecoderMediaType"] = video_decoder_media_type
        if video_decoder_hw_accel is not UNSET:
            field_dict["VideoDecoderHwAccel"] = video_decoder_hw_accel
        if video_encoder is not UNSET:
            field_dict["VideoEncoder"] = video_encoder
        if video_encoder_is_hardware is not UNSET:
            field_dict["VideoEncoderIsHardware"] = video_encoder_is_hardware
        if video_encoder_media_type is not UNSET:
            field_dict["VideoEncoderMediaType"] = video_encoder_media_type
        if video_encoder_hw_accel is not UNSET:
            field_dict["VideoEncoderHwAccel"] = video_encoder_hw_accel
        if video_pipeline_info is not UNSET:
            field_dict["VideoPipelineInfo"] = video_pipeline_info
        if subtitle_pipeline_infos is not UNSET:
            field_dict["SubtitlePipelineInfos"] = subtitle_pipeline_infos

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.process_run_metrics_process_statistics import ProcessRunMetricsProcessStatistics
        from ..models.transcoding_vp_step_info import TranscodingVpStepInfo
        from ..models.tuple_double_double import TupleDoubleDouble

        d = src_dict.copy()
        audio_codec = d.pop("AudioCodec", UNSET)

        video_codec = d.pop("VideoCodec", UNSET)

        sub_protocol = d.pop("SubProtocol", UNSET)

        container = d.pop("Container", UNSET)

        is_video_direct = d.pop("IsVideoDirect", UNSET)

        is_audio_direct = d.pop("IsAudioDirect", UNSET)

        bitrate = d.pop("Bitrate", UNSET)

        audio_bitrate = d.pop("AudioBitrate", UNSET)

        video_bitrate = d.pop("VideoBitrate", UNSET)

        framerate = d.pop("Framerate", UNSET)

        completion_percentage = d.pop("CompletionPercentage", UNSET)

        transcoding_position_ticks = d.pop("TranscodingPositionTicks", UNSET)

        transcoding_start_position_ticks = d.pop("TranscodingStartPositionTicks", UNSET)

        width = d.pop("Width", UNSET)

        height = d.pop("Height", UNSET)

        audio_channels = d.pop("AudioChannels", UNSET)

        transcode_reasons = []
        _transcode_reasons = d.pop("TranscodeReasons", UNSET)
        for transcode_reasons_item_data in _transcode_reasons or []:
            transcode_reasons_item = TranscodeReason(transcode_reasons_item_data)

            transcode_reasons.append(transcode_reasons_item)

        current_cpu_usage = d.pop("CurrentCpuUsage", UNSET)

        average_cpu_usage = d.pop("AverageCpuUsage", UNSET)

        cpu_history = []
        _cpu_history = d.pop("CpuHistory", UNSET)
        for cpu_history_item_data in _cpu_history or []:
            cpu_history_item = TupleDoubleDouble.from_dict(cpu_history_item_data)

            cpu_history.append(cpu_history_item)

        _process_statistics = d.pop("ProcessStatistics", UNSET)
        process_statistics: Union[Unset, ProcessRunMetricsProcessStatistics]
        if isinstance(_process_statistics, Unset):
            process_statistics = UNSET
        else:
            process_statistics = ProcessRunMetricsProcessStatistics.from_dict(_process_statistics)

        current_throttle = d.pop("CurrentThrottle", UNSET)

        video_decoder = d.pop("VideoDecoder", UNSET)

        video_decoder_is_hardware = d.pop("VideoDecoderIsHardware", UNSET)

        video_decoder_media_type = d.pop("VideoDecoderMediaType", UNSET)

        video_decoder_hw_accel = d.pop("VideoDecoderHwAccel", UNSET)

        video_encoder = d.pop("VideoEncoder", UNSET)

        video_encoder_is_hardware = d.pop("VideoEncoderIsHardware", UNSET)

        video_encoder_media_type = d.pop("VideoEncoderMediaType", UNSET)

        video_encoder_hw_accel = d.pop("VideoEncoderHwAccel", UNSET)

        video_pipeline_info = []
        _video_pipeline_info = d.pop("VideoPipelineInfo", UNSET)
        for video_pipeline_info_item_data in _video_pipeline_info or []:
            video_pipeline_info_item = TranscodingVpStepInfo.from_dict(video_pipeline_info_item_data)

            video_pipeline_info.append(video_pipeline_info_item)

        subtitle_pipeline_infos = []
        _subtitle_pipeline_infos = d.pop("SubtitlePipelineInfos", UNSET)
        for subtitle_pipeline_infos_item_data in _subtitle_pipeline_infos or []:
            subtitle_pipeline_infos_item = []
            _subtitle_pipeline_infos_item = subtitle_pipeline_infos_item_data
            for subtitle_pipeline_infos_item_item_data in _subtitle_pipeline_infos_item:
                subtitle_pipeline_infos_item_item = TranscodingVpStepInfo.from_dict(
                    subtitle_pipeline_infos_item_item_data
                )

                subtitle_pipeline_infos_item.append(subtitle_pipeline_infos_item_item)

            subtitle_pipeline_infos.append(subtitle_pipeline_infos_item)

        transcoding_info = cls(
            audio_codec=audio_codec,
            video_codec=video_codec,
            sub_protocol=sub_protocol,
            container=container,
            is_video_direct=is_video_direct,
            is_audio_direct=is_audio_direct,
            bitrate=bitrate,
            audio_bitrate=audio_bitrate,
            video_bitrate=video_bitrate,
            framerate=framerate,
            completion_percentage=completion_percentage,
            transcoding_position_ticks=transcoding_position_ticks,
            transcoding_start_position_ticks=transcoding_start_position_ticks,
            width=width,
            height=height,
            audio_channels=audio_channels,
            transcode_reasons=transcode_reasons,
            current_cpu_usage=current_cpu_usage,
            average_cpu_usage=average_cpu_usage,
            cpu_history=cpu_history,
            process_statistics=process_statistics,
            current_throttle=current_throttle,
            video_decoder=video_decoder,
            video_decoder_is_hardware=video_decoder_is_hardware,
            video_decoder_media_type=video_decoder_media_type,
            video_decoder_hw_accel=video_decoder_hw_accel,
            video_encoder=video_encoder,
            video_encoder_is_hardware=video_encoder_is_hardware,
            video_encoder_media_type=video_encoder_media_type,
            video_encoder_hw_accel=video_encoder_hw_accel,
            video_pipeline_info=video_pipeline_info,
            subtitle_pipeline_infos=subtitle_pipeline_infos,
        )

        transcoding_info.additional_properties = d
        return transcoding_info

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
