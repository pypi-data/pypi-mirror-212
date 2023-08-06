from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dlna_subtitle_delivery_method import DlnaSubtitleDeliveryMethod
from ..models.extended_video_sub_types import ExtendedVideoSubTypes
from ..models.extended_video_types import ExtendedVideoTypes
from ..models.media_info_media_protocol import MediaInfoMediaProtocol
from ..models.media_stream_type import MediaStreamType
from ..models.subtitle_location_type import SubtitleLocationType
from ..types import UNSET, Unset

T = TypeVar("T", bound="MediaStream")


@attr.s(auto_attribs=True)
class MediaStream:
    """
    Attributes:
        codec (Union[Unset, str]):
        codec_tag (Union[Unset, str]):
        language (Union[Unset, str]):
        color_transfer (Union[Unset, str]):
        color_primaries (Union[Unset, str]):
        color_space (Union[Unset, str]):
        comment (Union[Unset, str]):
        stream_start_time_ticks (Union[Unset, None, int]):
        time_base (Union[Unset, str]):
        title (Union[Unset, str]):
        extradata (Union[Unset, str]):
        video_range (Union[Unset, str]):
        display_title (Union[Unset, str]):
        display_language (Union[Unset, str]):
        nal_length_size (Union[Unset, str]):
        is_interlaced (Union[Unset, bool]):
        is_avc (Union[Unset, None, bool]):
        channel_layout (Union[Unset, str]):
        bit_rate (Union[Unset, None, int]):
        bit_depth (Union[Unset, None, int]):
        ref_frames (Union[Unset, None, int]):
        rotation (Union[Unset, None, int]):
        channels (Union[Unset, None, int]):
        sample_rate (Union[Unset, None, int]):
        is_default (Union[Unset, bool]):
        is_forced (Union[Unset, bool]):
        height (Union[Unset, None, int]):
        width (Union[Unset, None, int]):
        average_frame_rate (Union[Unset, None, float]):
        real_frame_rate (Union[Unset, None, float]):
        profile (Union[Unset, str]):
        type (Union[Unset, MediaStreamType]):
        aspect_ratio (Union[Unset, str]):
        index (Union[Unset, int]):
        is_external (Union[Unset, bool]):
        delivery_method (Union[Unset, DlnaSubtitleDeliveryMethod]):
        delivery_url (Union[Unset, str]):
        is_external_url (Union[Unset, None, bool]):
        is_text_subtitle_stream (Union[Unset, bool]):
        supports_external_stream (Union[Unset, bool]):
        path (Union[Unset, str]):
        protocol (Union[Unset, MediaInfoMediaProtocol]):
        pixel_format (Union[Unset, str]):
        level (Union[Unset, None, float]):
        is_anamorphic (Union[Unset, None, bool]):
        extended_video_type (Union[Unset, ExtendedVideoTypes]):
        extended_video_subtype (Union[Unset, ExtendedVideoSubTypes]):
        item_id (Union[Unset, str]):
        server_id (Union[Unset, str]):
        attachment_size (Union[Unset, None, int]):
        mime_type (Union[Unset, str]):
        subtitle_location_type (Union[Unset, SubtitleLocationType]):
    """

    codec: Union[Unset, str] = UNSET
    codec_tag: Union[Unset, str] = UNSET
    language: Union[Unset, str] = UNSET
    color_transfer: Union[Unset, str] = UNSET
    color_primaries: Union[Unset, str] = UNSET
    color_space: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    stream_start_time_ticks: Union[Unset, None, int] = UNSET
    time_base: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    extradata: Union[Unset, str] = UNSET
    video_range: Union[Unset, str] = UNSET
    display_title: Union[Unset, str] = UNSET
    display_language: Union[Unset, str] = UNSET
    nal_length_size: Union[Unset, str] = UNSET
    is_interlaced: Union[Unset, bool] = UNSET
    is_avc: Union[Unset, None, bool] = UNSET
    channel_layout: Union[Unset, str] = UNSET
    bit_rate: Union[Unset, None, int] = UNSET
    bit_depth: Union[Unset, None, int] = UNSET
    ref_frames: Union[Unset, None, int] = UNSET
    rotation: Union[Unset, None, int] = UNSET
    channels: Union[Unset, None, int] = UNSET
    sample_rate: Union[Unset, None, int] = UNSET
    is_default: Union[Unset, bool] = UNSET
    is_forced: Union[Unset, bool] = UNSET
    height: Union[Unset, None, int] = UNSET
    width: Union[Unset, None, int] = UNSET
    average_frame_rate: Union[Unset, None, float] = UNSET
    real_frame_rate: Union[Unset, None, float] = UNSET
    profile: Union[Unset, str] = UNSET
    type: Union[Unset, MediaStreamType] = UNSET
    aspect_ratio: Union[Unset, str] = UNSET
    index: Union[Unset, int] = UNSET
    is_external: Union[Unset, bool] = UNSET
    delivery_method: Union[Unset, DlnaSubtitleDeliveryMethod] = UNSET
    delivery_url: Union[Unset, str] = UNSET
    is_external_url: Union[Unset, None, bool] = UNSET
    is_text_subtitle_stream: Union[Unset, bool] = UNSET
    supports_external_stream: Union[Unset, bool] = UNSET
    path: Union[Unset, str] = UNSET
    protocol: Union[Unset, MediaInfoMediaProtocol] = UNSET
    pixel_format: Union[Unset, str] = UNSET
    level: Union[Unset, None, float] = UNSET
    is_anamorphic: Union[Unset, None, bool] = UNSET
    extended_video_type: Union[Unset, ExtendedVideoTypes] = UNSET
    extended_video_subtype: Union[Unset, ExtendedVideoSubTypes] = UNSET
    item_id: Union[Unset, str] = UNSET
    server_id: Union[Unset, str] = UNSET
    attachment_size: Union[Unset, None, int] = UNSET
    mime_type: Union[Unset, str] = UNSET
    subtitle_location_type: Union[Unset, SubtitleLocationType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        codec = self.codec
        codec_tag = self.codec_tag
        language = self.language
        color_transfer = self.color_transfer
        color_primaries = self.color_primaries
        color_space = self.color_space
        comment = self.comment
        stream_start_time_ticks = self.stream_start_time_ticks
        time_base = self.time_base
        title = self.title
        extradata = self.extradata
        video_range = self.video_range
        display_title = self.display_title
        display_language = self.display_language
        nal_length_size = self.nal_length_size
        is_interlaced = self.is_interlaced
        is_avc = self.is_avc
        channel_layout = self.channel_layout
        bit_rate = self.bit_rate
        bit_depth = self.bit_depth
        ref_frames = self.ref_frames
        rotation = self.rotation
        channels = self.channels
        sample_rate = self.sample_rate
        is_default = self.is_default
        is_forced = self.is_forced
        height = self.height
        width = self.width
        average_frame_rate = self.average_frame_rate
        real_frame_rate = self.real_frame_rate
        profile = self.profile
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        aspect_ratio = self.aspect_ratio
        index = self.index
        is_external = self.is_external
        delivery_method: Union[Unset, str] = UNSET
        if not isinstance(self.delivery_method, Unset):
            delivery_method = self.delivery_method.value

        delivery_url = self.delivery_url
        is_external_url = self.is_external_url
        is_text_subtitle_stream = self.is_text_subtitle_stream
        supports_external_stream = self.supports_external_stream
        path = self.path
        protocol: Union[Unset, str] = UNSET
        if not isinstance(self.protocol, Unset):
            protocol = self.protocol.value

        pixel_format = self.pixel_format
        level = self.level
        is_anamorphic = self.is_anamorphic
        extended_video_type: Union[Unset, str] = UNSET
        if not isinstance(self.extended_video_type, Unset):
            extended_video_type = self.extended_video_type.value

        extended_video_subtype: Union[Unset, str] = UNSET
        if not isinstance(self.extended_video_subtype, Unset):
            extended_video_subtype = self.extended_video_subtype.value

        item_id = self.item_id
        server_id = self.server_id
        attachment_size = self.attachment_size
        mime_type = self.mime_type
        subtitle_location_type: Union[Unset, str] = UNSET
        if not isinstance(self.subtitle_location_type, Unset):
            subtitle_location_type = self.subtitle_location_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if codec is not UNSET:
            field_dict["Codec"] = codec
        if codec_tag is not UNSET:
            field_dict["CodecTag"] = codec_tag
        if language is not UNSET:
            field_dict["Language"] = language
        if color_transfer is not UNSET:
            field_dict["ColorTransfer"] = color_transfer
        if color_primaries is not UNSET:
            field_dict["ColorPrimaries"] = color_primaries
        if color_space is not UNSET:
            field_dict["ColorSpace"] = color_space
        if comment is not UNSET:
            field_dict["Comment"] = comment
        if stream_start_time_ticks is not UNSET:
            field_dict["StreamStartTimeTicks"] = stream_start_time_ticks
        if time_base is not UNSET:
            field_dict["TimeBase"] = time_base
        if title is not UNSET:
            field_dict["Title"] = title
        if extradata is not UNSET:
            field_dict["Extradata"] = extradata
        if video_range is not UNSET:
            field_dict["VideoRange"] = video_range
        if display_title is not UNSET:
            field_dict["DisplayTitle"] = display_title
        if display_language is not UNSET:
            field_dict["DisplayLanguage"] = display_language
        if nal_length_size is not UNSET:
            field_dict["NalLengthSize"] = nal_length_size
        if is_interlaced is not UNSET:
            field_dict["IsInterlaced"] = is_interlaced
        if is_avc is not UNSET:
            field_dict["IsAVC"] = is_avc
        if channel_layout is not UNSET:
            field_dict["ChannelLayout"] = channel_layout
        if bit_rate is not UNSET:
            field_dict["BitRate"] = bit_rate
        if bit_depth is not UNSET:
            field_dict["BitDepth"] = bit_depth
        if ref_frames is not UNSET:
            field_dict["RefFrames"] = ref_frames
        if rotation is not UNSET:
            field_dict["Rotation"] = rotation
        if channels is not UNSET:
            field_dict["Channels"] = channels
        if sample_rate is not UNSET:
            field_dict["SampleRate"] = sample_rate
        if is_default is not UNSET:
            field_dict["IsDefault"] = is_default
        if is_forced is not UNSET:
            field_dict["IsForced"] = is_forced
        if height is not UNSET:
            field_dict["Height"] = height
        if width is not UNSET:
            field_dict["Width"] = width
        if average_frame_rate is not UNSET:
            field_dict["AverageFrameRate"] = average_frame_rate
        if real_frame_rate is not UNSET:
            field_dict["RealFrameRate"] = real_frame_rate
        if profile is not UNSET:
            field_dict["Profile"] = profile
        if type is not UNSET:
            field_dict["Type"] = type
        if aspect_ratio is not UNSET:
            field_dict["AspectRatio"] = aspect_ratio
        if index is not UNSET:
            field_dict["Index"] = index
        if is_external is not UNSET:
            field_dict["IsExternal"] = is_external
        if delivery_method is not UNSET:
            field_dict["DeliveryMethod"] = delivery_method
        if delivery_url is not UNSET:
            field_dict["DeliveryUrl"] = delivery_url
        if is_external_url is not UNSET:
            field_dict["IsExternalUrl"] = is_external_url
        if is_text_subtitle_stream is not UNSET:
            field_dict["IsTextSubtitleStream"] = is_text_subtitle_stream
        if supports_external_stream is not UNSET:
            field_dict["SupportsExternalStream"] = supports_external_stream
        if path is not UNSET:
            field_dict["Path"] = path
        if protocol is not UNSET:
            field_dict["Protocol"] = protocol
        if pixel_format is not UNSET:
            field_dict["PixelFormat"] = pixel_format
        if level is not UNSET:
            field_dict["Level"] = level
        if is_anamorphic is not UNSET:
            field_dict["IsAnamorphic"] = is_anamorphic
        if extended_video_type is not UNSET:
            field_dict["ExtendedVideoType"] = extended_video_type
        if extended_video_subtype is not UNSET:
            field_dict["ExtendedVideoSubtype"] = extended_video_subtype
        if item_id is not UNSET:
            field_dict["ItemId"] = item_id
        if server_id is not UNSET:
            field_dict["ServerId"] = server_id
        if attachment_size is not UNSET:
            field_dict["AttachmentSize"] = attachment_size
        if mime_type is not UNSET:
            field_dict["MimeType"] = mime_type
        if subtitle_location_type is not UNSET:
            field_dict["SubtitleLocationType"] = subtitle_location_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        codec = d.pop("Codec", UNSET)

        codec_tag = d.pop("CodecTag", UNSET)

        language = d.pop("Language", UNSET)

        color_transfer = d.pop("ColorTransfer", UNSET)

        color_primaries = d.pop("ColorPrimaries", UNSET)

        color_space = d.pop("ColorSpace", UNSET)

        comment = d.pop("Comment", UNSET)

        stream_start_time_ticks = d.pop("StreamStartTimeTicks", UNSET)

        time_base = d.pop("TimeBase", UNSET)

        title = d.pop("Title", UNSET)

        extradata = d.pop("Extradata", UNSET)

        video_range = d.pop("VideoRange", UNSET)

        display_title = d.pop("DisplayTitle", UNSET)

        display_language = d.pop("DisplayLanguage", UNSET)

        nal_length_size = d.pop("NalLengthSize", UNSET)

        is_interlaced = d.pop("IsInterlaced", UNSET)

        is_avc = d.pop("IsAVC", UNSET)

        channel_layout = d.pop("ChannelLayout", UNSET)

        bit_rate = d.pop("BitRate", UNSET)

        bit_depth = d.pop("BitDepth", UNSET)

        ref_frames = d.pop("RefFrames", UNSET)

        rotation = d.pop("Rotation", UNSET)

        channels = d.pop("Channels", UNSET)

        sample_rate = d.pop("SampleRate", UNSET)

        is_default = d.pop("IsDefault", UNSET)

        is_forced = d.pop("IsForced", UNSET)

        height = d.pop("Height", UNSET)

        width = d.pop("Width", UNSET)

        average_frame_rate = d.pop("AverageFrameRate", UNSET)

        real_frame_rate = d.pop("RealFrameRate", UNSET)

        profile = d.pop("Profile", UNSET)

        _type = d.pop("Type", UNSET)
        type: Union[Unset, MediaStreamType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = MediaStreamType(_type)

        aspect_ratio = d.pop("AspectRatio", UNSET)

        index = d.pop("Index", UNSET)

        is_external = d.pop("IsExternal", UNSET)

        _delivery_method = d.pop("DeliveryMethod", UNSET)
        delivery_method: Union[Unset, DlnaSubtitleDeliveryMethod]
        if isinstance(_delivery_method, Unset):
            delivery_method = UNSET
        else:
            delivery_method = DlnaSubtitleDeliveryMethod(_delivery_method)

        delivery_url = d.pop("DeliveryUrl", UNSET)

        is_external_url = d.pop("IsExternalUrl", UNSET)

        is_text_subtitle_stream = d.pop("IsTextSubtitleStream", UNSET)

        supports_external_stream = d.pop("SupportsExternalStream", UNSET)

        path = d.pop("Path", UNSET)

        _protocol = d.pop("Protocol", UNSET)
        protocol: Union[Unset, MediaInfoMediaProtocol]
        if isinstance(_protocol, Unset):
            protocol = UNSET
        else:
            protocol = MediaInfoMediaProtocol(_protocol)

        pixel_format = d.pop("PixelFormat", UNSET)

        level = d.pop("Level", UNSET)

        is_anamorphic = d.pop("IsAnamorphic", UNSET)

        _extended_video_type = d.pop("ExtendedVideoType", UNSET)
        extended_video_type: Union[Unset, ExtendedVideoTypes]
        if isinstance(_extended_video_type, Unset):
            extended_video_type = UNSET
        else:
            extended_video_type = ExtendedVideoTypes(_extended_video_type)

        _extended_video_subtype = d.pop("ExtendedVideoSubtype", UNSET)
        extended_video_subtype: Union[Unset, ExtendedVideoSubTypes]
        if isinstance(_extended_video_subtype, Unset):
            extended_video_subtype = UNSET
        else:
            extended_video_subtype = ExtendedVideoSubTypes(_extended_video_subtype)

        item_id = d.pop("ItemId", UNSET)

        server_id = d.pop("ServerId", UNSET)

        attachment_size = d.pop("AttachmentSize", UNSET)

        mime_type = d.pop("MimeType", UNSET)

        _subtitle_location_type = d.pop("SubtitleLocationType", UNSET)
        subtitle_location_type: Union[Unset, SubtitleLocationType]
        if isinstance(_subtitle_location_type, Unset):
            subtitle_location_type = UNSET
        else:
            subtitle_location_type = SubtitleLocationType(_subtitle_location_type)

        media_stream = cls(
            codec=codec,
            codec_tag=codec_tag,
            language=language,
            color_transfer=color_transfer,
            color_primaries=color_primaries,
            color_space=color_space,
            comment=comment,
            stream_start_time_ticks=stream_start_time_ticks,
            time_base=time_base,
            title=title,
            extradata=extradata,
            video_range=video_range,
            display_title=display_title,
            display_language=display_language,
            nal_length_size=nal_length_size,
            is_interlaced=is_interlaced,
            is_avc=is_avc,
            channel_layout=channel_layout,
            bit_rate=bit_rate,
            bit_depth=bit_depth,
            ref_frames=ref_frames,
            rotation=rotation,
            channels=channels,
            sample_rate=sample_rate,
            is_default=is_default,
            is_forced=is_forced,
            height=height,
            width=width,
            average_frame_rate=average_frame_rate,
            real_frame_rate=real_frame_rate,
            profile=profile,
            type=type,
            aspect_ratio=aspect_ratio,
            index=index,
            is_external=is_external,
            delivery_method=delivery_method,
            delivery_url=delivery_url,
            is_external_url=is_external_url,
            is_text_subtitle_stream=is_text_subtitle_stream,
            supports_external_stream=supports_external_stream,
            path=path,
            protocol=protocol,
            pixel_format=pixel_format,
            level=level,
            is_anamorphic=is_anamorphic,
            extended_video_type=extended_video_type,
            extended_video_subtype=extended_video_subtype,
            item_id=item_id,
            server_id=server_id,
            attachment_size=attachment_size,
            mime_type=mime_type,
            subtitle_location_type=subtitle_location_type,
        )

        media_stream.additional_properties = d
        return media_stream

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
