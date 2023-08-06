from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.media_info_media_protocol import MediaInfoMediaProtocol
from ..models.media_info_transport_stream_timestamp import MediaInfoTransportStreamTimestamp
from ..models.media_source_type import MediaSourceType
from ..models.video_3d_format import Video3DFormat
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.media_source_info_required_http_headers import MediaSourceInfoRequiredHttpHeaders
    from ..models.media_stream import MediaStream


T = TypeVar("T", bound="MediaSourceInfo")


@attr.s(auto_attribs=True)
class MediaSourceInfo:
    """
    Attributes:
        protocol (Union[Unset, MediaInfoMediaProtocol]):
        id (Union[Unset, str]):
        path (Union[Unset, str]):
        encoder_path (Union[Unset, str]):
        encoder_protocol (Union[Unset, MediaInfoMediaProtocol]):
        type (Union[Unset, MediaSourceType]):
        container (Union[Unset, str]):
        size (Union[Unset, None, int]):
        name (Union[Unset, str]):
        sort_name (Union[Unset, str]):
        is_remote (Union[Unset, bool]):
        run_time_ticks (Union[Unset, None, int]):
        container_start_time_ticks (Union[Unset, None, int]):
        supports_transcoding (Union[Unset, bool]):
        supports_direct_stream (Union[Unset, bool]):
        supports_direct_play (Union[Unset, bool]):
        is_infinite_stream (Union[Unset, bool]):
        requires_opening (Union[Unset, bool]):
        open_token (Union[Unset, str]):
        requires_closing (Union[Unset, bool]):
        live_stream_id (Union[Unset, str]):
        buffer_ms (Union[Unset, None, int]):
        requires_looping (Union[Unset, bool]):
        supports_probing (Union[Unset, bool]):
        video_3d_format (Union[Unset, Video3DFormat]):
        media_streams (Union[Unset, List['MediaStream']]):
        formats (Union[Unset, List[str]]):
        bitrate (Union[Unset, None, int]):
        timestamp (Union[Unset, MediaInfoTransportStreamTimestamp]):
        required_http_headers (Union[Unset, MediaSourceInfoRequiredHttpHeaders]):
        direct_stream_url (Union[Unset, str]):
        transcoding_url (Union[Unset, str]):
        transcoding_sub_protocol (Union[Unset, str]):
        transcoding_container (Union[Unset, str]):
        analyze_duration_ms (Union[Unset, None, int]):
        read_at_native_framerate (Union[Unset, bool]):
        default_audio_stream_index (Union[Unset, None, int]):
        default_subtitle_stream_index (Union[Unset, None, int]):
        item_id (Union[Unset, str]):
        server_id (Union[Unset, str]):
    """

    protocol: Union[Unset, MediaInfoMediaProtocol] = UNSET
    id: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    encoder_path: Union[Unset, str] = UNSET
    encoder_protocol: Union[Unset, MediaInfoMediaProtocol] = UNSET
    type: Union[Unset, MediaSourceType] = UNSET
    container: Union[Unset, str] = UNSET
    size: Union[Unset, None, int] = UNSET
    name: Union[Unset, str] = UNSET
    sort_name: Union[Unset, str] = UNSET
    is_remote: Union[Unset, bool] = UNSET
    run_time_ticks: Union[Unset, None, int] = UNSET
    container_start_time_ticks: Union[Unset, None, int] = UNSET
    supports_transcoding: Union[Unset, bool] = UNSET
    supports_direct_stream: Union[Unset, bool] = UNSET
    supports_direct_play: Union[Unset, bool] = UNSET
    is_infinite_stream: Union[Unset, bool] = UNSET
    requires_opening: Union[Unset, bool] = UNSET
    open_token: Union[Unset, str] = UNSET
    requires_closing: Union[Unset, bool] = UNSET
    live_stream_id: Union[Unset, str] = UNSET
    buffer_ms: Union[Unset, None, int] = UNSET
    requires_looping: Union[Unset, bool] = UNSET
    supports_probing: Union[Unset, bool] = UNSET
    video_3d_format: Union[Unset, Video3DFormat] = UNSET
    media_streams: Union[Unset, List["MediaStream"]] = UNSET
    formats: Union[Unset, List[str]] = UNSET
    bitrate: Union[Unset, None, int] = UNSET
    timestamp: Union[Unset, MediaInfoTransportStreamTimestamp] = UNSET
    required_http_headers: Union[Unset, "MediaSourceInfoRequiredHttpHeaders"] = UNSET
    direct_stream_url: Union[Unset, str] = UNSET
    transcoding_url: Union[Unset, str] = UNSET
    transcoding_sub_protocol: Union[Unset, str] = UNSET
    transcoding_container: Union[Unset, str] = UNSET
    analyze_duration_ms: Union[Unset, None, int] = UNSET
    read_at_native_framerate: Union[Unset, bool] = UNSET
    default_audio_stream_index: Union[Unset, None, int] = UNSET
    default_subtitle_stream_index: Union[Unset, None, int] = UNSET
    item_id: Union[Unset, str] = UNSET
    server_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        protocol: Union[Unset, str] = UNSET
        if not isinstance(self.protocol, Unset):
            protocol = self.protocol.value

        id = self.id
        path = self.path
        encoder_path = self.encoder_path
        encoder_protocol: Union[Unset, str] = UNSET
        if not isinstance(self.encoder_protocol, Unset):
            encoder_protocol = self.encoder_protocol.value

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        container = self.container
        size = self.size
        name = self.name
        sort_name = self.sort_name
        is_remote = self.is_remote
        run_time_ticks = self.run_time_ticks
        container_start_time_ticks = self.container_start_time_ticks
        supports_transcoding = self.supports_transcoding
        supports_direct_stream = self.supports_direct_stream
        supports_direct_play = self.supports_direct_play
        is_infinite_stream = self.is_infinite_stream
        requires_opening = self.requires_opening
        open_token = self.open_token
        requires_closing = self.requires_closing
        live_stream_id = self.live_stream_id
        buffer_ms = self.buffer_ms
        requires_looping = self.requires_looping
        supports_probing = self.supports_probing
        video_3d_format: Union[Unset, str] = UNSET
        if not isinstance(self.video_3d_format, Unset):
            video_3d_format = self.video_3d_format.value

        media_streams: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.media_streams, Unset):
            media_streams = []
            for media_streams_item_data in self.media_streams:
                media_streams_item = media_streams_item_data.to_dict()

                media_streams.append(media_streams_item)

        formats: Union[Unset, List[str]] = UNSET
        if not isinstance(self.formats, Unset):
            formats = self.formats

        bitrate = self.bitrate
        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.value

        required_http_headers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.required_http_headers, Unset):
            required_http_headers = self.required_http_headers.to_dict()

        direct_stream_url = self.direct_stream_url
        transcoding_url = self.transcoding_url
        transcoding_sub_protocol = self.transcoding_sub_protocol
        transcoding_container = self.transcoding_container
        analyze_duration_ms = self.analyze_duration_ms
        read_at_native_framerate = self.read_at_native_framerate
        default_audio_stream_index = self.default_audio_stream_index
        default_subtitle_stream_index = self.default_subtitle_stream_index
        item_id = self.item_id
        server_id = self.server_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if protocol is not UNSET:
            field_dict["Protocol"] = protocol
        if id is not UNSET:
            field_dict["Id"] = id
        if path is not UNSET:
            field_dict["Path"] = path
        if encoder_path is not UNSET:
            field_dict["EncoderPath"] = encoder_path
        if encoder_protocol is not UNSET:
            field_dict["EncoderProtocol"] = encoder_protocol
        if type is not UNSET:
            field_dict["Type"] = type
        if container is not UNSET:
            field_dict["Container"] = container
        if size is not UNSET:
            field_dict["Size"] = size
        if name is not UNSET:
            field_dict["Name"] = name
        if sort_name is not UNSET:
            field_dict["SortName"] = sort_name
        if is_remote is not UNSET:
            field_dict["IsRemote"] = is_remote
        if run_time_ticks is not UNSET:
            field_dict["RunTimeTicks"] = run_time_ticks
        if container_start_time_ticks is not UNSET:
            field_dict["ContainerStartTimeTicks"] = container_start_time_ticks
        if supports_transcoding is not UNSET:
            field_dict["SupportsTranscoding"] = supports_transcoding
        if supports_direct_stream is not UNSET:
            field_dict["SupportsDirectStream"] = supports_direct_stream
        if supports_direct_play is not UNSET:
            field_dict["SupportsDirectPlay"] = supports_direct_play
        if is_infinite_stream is not UNSET:
            field_dict["IsInfiniteStream"] = is_infinite_stream
        if requires_opening is not UNSET:
            field_dict["RequiresOpening"] = requires_opening
        if open_token is not UNSET:
            field_dict["OpenToken"] = open_token
        if requires_closing is not UNSET:
            field_dict["RequiresClosing"] = requires_closing
        if live_stream_id is not UNSET:
            field_dict["LiveStreamId"] = live_stream_id
        if buffer_ms is not UNSET:
            field_dict["BufferMs"] = buffer_ms
        if requires_looping is not UNSET:
            field_dict["RequiresLooping"] = requires_looping
        if supports_probing is not UNSET:
            field_dict["SupportsProbing"] = supports_probing
        if video_3d_format is not UNSET:
            field_dict["Video3DFormat"] = video_3d_format
        if media_streams is not UNSET:
            field_dict["MediaStreams"] = media_streams
        if formats is not UNSET:
            field_dict["Formats"] = formats
        if bitrate is not UNSET:
            field_dict["Bitrate"] = bitrate
        if timestamp is not UNSET:
            field_dict["Timestamp"] = timestamp
        if required_http_headers is not UNSET:
            field_dict["RequiredHttpHeaders"] = required_http_headers
        if direct_stream_url is not UNSET:
            field_dict["DirectStreamUrl"] = direct_stream_url
        if transcoding_url is not UNSET:
            field_dict["TranscodingUrl"] = transcoding_url
        if transcoding_sub_protocol is not UNSET:
            field_dict["TranscodingSubProtocol"] = transcoding_sub_protocol
        if transcoding_container is not UNSET:
            field_dict["TranscodingContainer"] = transcoding_container
        if analyze_duration_ms is not UNSET:
            field_dict["AnalyzeDurationMs"] = analyze_duration_ms
        if read_at_native_framerate is not UNSET:
            field_dict["ReadAtNativeFramerate"] = read_at_native_framerate
        if default_audio_stream_index is not UNSET:
            field_dict["DefaultAudioStreamIndex"] = default_audio_stream_index
        if default_subtitle_stream_index is not UNSET:
            field_dict["DefaultSubtitleStreamIndex"] = default_subtitle_stream_index
        if item_id is not UNSET:
            field_dict["ItemId"] = item_id
        if server_id is not UNSET:
            field_dict["ServerId"] = server_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.media_source_info_required_http_headers import MediaSourceInfoRequiredHttpHeaders
        from ..models.media_stream import MediaStream

        d = src_dict.copy()
        _protocol = d.pop("Protocol", UNSET)
        protocol: Union[Unset, MediaInfoMediaProtocol]
        if isinstance(_protocol, Unset):
            protocol = UNSET
        else:
            protocol = MediaInfoMediaProtocol(_protocol)

        id = d.pop("Id", UNSET)

        path = d.pop("Path", UNSET)

        encoder_path = d.pop("EncoderPath", UNSET)

        _encoder_protocol = d.pop("EncoderProtocol", UNSET)
        encoder_protocol: Union[Unset, MediaInfoMediaProtocol]
        if isinstance(_encoder_protocol, Unset):
            encoder_protocol = UNSET
        else:
            encoder_protocol = MediaInfoMediaProtocol(_encoder_protocol)

        _type = d.pop("Type", UNSET)
        type: Union[Unset, MediaSourceType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = MediaSourceType(_type)

        container = d.pop("Container", UNSET)

        size = d.pop("Size", UNSET)

        name = d.pop("Name", UNSET)

        sort_name = d.pop("SortName", UNSET)

        is_remote = d.pop("IsRemote", UNSET)

        run_time_ticks = d.pop("RunTimeTicks", UNSET)

        container_start_time_ticks = d.pop("ContainerStartTimeTicks", UNSET)

        supports_transcoding = d.pop("SupportsTranscoding", UNSET)

        supports_direct_stream = d.pop("SupportsDirectStream", UNSET)

        supports_direct_play = d.pop("SupportsDirectPlay", UNSET)

        is_infinite_stream = d.pop("IsInfiniteStream", UNSET)

        requires_opening = d.pop("RequiresOpening", UNSET)

        open_token = d.pop("OpenToken", UNSET)

        requires_closing = d.pop("RequiresClosing", UNSET)

        live_stream_id = d.pop("LiveStreamId", UNSET)

        buffer_ms = d.pop("BufferMs", UNSET)

        requires_looping = d.pop("RequiresLooping", UNSET)

        supports_probing = d.pop("SupportsProbing", UNSET)

        _video_3d_format = d.pop("Video3DFormat", UNSET)
        video_3d_format: Union[Unset, Video3DFormat]
        if isinstance(_video_3d_format, Unset):
            video_3d_format = UNSET
        else:
            video_3d_format = Video3DFormat(_video_3d_format)

        media_streams = []
        _media_streams = d.pop("MediaStreams", UNSET)
        for media_streams_item_data in _media_streams or []:
            media_streams_item = MediaStream.from_dict(media_streams_item_data)

            media_streams.append(media_streams_item)

        formats = cast(List[str], d.pop("Formats", UNSET))

        bitrate = d.pop("Bitrate", UNSET)

        _timestamp = d.pop("Timestamp", UNSET)
        timestamp: Union[Unset, MediaInfoTransportStreamTimestamp]
        if isinstance(_timestamp, Unset):
            timestamp = UNSET
        else:
            timestamp = MediaInfoTransportStreamTimestamp(_timestamp)

        _required_http_headers = d.pop("RequiredHttpHeaders", UNSET)
        required_http_headers: Union[Unset, MediaSourceInfoRequiredHttpHeaders]
        if isinstance(_required_http_headers, Unset):
            required_http_headers = UNSET
        else:
            required_http_headers = MediaSourceInfoRequiredHttpHeaders.from_dict(_required_http_headers)

        direct_stream_url = d.pop("DirectStreamUrl", UNSET)

        transcoding_url = d.pop("TranscodingUrl", UNSET)

        transcoding_sub_protocol = d.pop("TranscodingSubProtocol", UNSET)

        transcoding_container = d.pop("TranscodingContainer", UNSET)

        analyze_duration_ms = d.pop("AnalyzeDurationMs", UNSET)

        read_at_native_framerate = d.pop("ReadAtNativeFramerate", UNSET)

        default_audio_stream_index = d.pop("DefaultAudioStreamIndex", UNSET)

        default_subtitle_stream_index = d.pop("DefaultSubtitleStreamIndex", UNSET)

        item_id = d.pop("ItemId", UNSET)

        server_id = d.pop("ServerId", UNSET)

        media_source_info = cls(
            protocol=protocol,
            id=id,
            path=path,
            encoder_path=encoder_path,
            encoder_protocol=encoder_protocol,
            type=type,
            container=container,
            size=size,
            name=name,
            sort_name=sort_name,
            is_remote=is_remote,
            run_time_ticks=run_time_ticks,
            container_start_time_ticks=container_start_time_ticks,
            supports_transcoding=supports_transcoding,
            supports_direct_stream=supports_direct_stream,
            supports_direct_play=supports_direct_play,
            is_infinite_stream=is_infinite_stream,
            requires_opening=requires_opening,
            open_token=open_token,
            requires_closing=requires_closing,
            live_stream_id=live_stream_id,
            buffer_ms=buffer_ms,
            requires_looping=requires_looping,
            supports_probing=supports_probing,
            video_3d_format=video_3d_format,
            media_streams=media_streams,
            formats=formats,
            bitrate=bitrate,
            timestamp=timestamp,
            required_http_headers=required_http_headers,
            direct_stream_url=direct_stream_url,
            transcoding_url=transcoding_url,
            transcoding_sub_protocol=transcoding_sub_protocol,
            transcoding_container=transcoding_container,
            analyze_duration_ms=analyze_duration_ms,
            read_at_native_framerate=read_at_native_framerate,
            default_audio_stream_index=default_audio_stream_index,
            default_subtitle_stream_index=default_subtitle_stream_index,
            item_id=item_id,
            server_id=server_id,
        )

        media_source_info.additional_properties = d
        return media_source_info

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
