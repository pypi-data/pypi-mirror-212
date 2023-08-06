from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.emby_dlna_profiles_device_profile_type import EmbyDlnaProfilesDeviceProfileType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dlna_codec_profile import DlnaCodecProfile
    from ..models.dlna_container_profile import DlnaContainerProfile
    from ..models.dlna_direct_play_profile import DlnaDirectPlayProfile
    from ..models.dlna_response_profile import DlnaResponseProfile
    from ..models.dlna_subtitle_profile import DlnaSubtitleProfile
    from ..models.dlna_transcoding_profile import DlnaTranscodingProfile
    from ..models.emby_dlna_profiles_device_identification import EmbyDlnaProfilesDeviceIdentification
    from ..models.emby_dlna_profiles_protocol_info_detection import EmbyDlnaProfilesProtocolInfoDetection


T = TypeVar("T", bound="EmbyDlnaProfilesDlnaProfile")


@attr.s(auto_attribs=True)
class EmbyDlnaProfilesDlnaProfile:
    """
    Attributes:
        type (Union[Unset, EmbyDlnaProfilesDeviceProfileType]):
        path (Union[Unset, str]):
        user_id (Union[Unset, str]):
        album_art_pn (Union[Unset, str]):
        max_album_art_width (Union[Unset, int]):
        max_album_art_height (Union[Unset, int]):
        max_icon_width (Union[Unset, None, int]):
        max_icon_height (Union[Unset, None, int]):
        friendly_name (Union[Unset, str]):
        manufacturer (Union[Unset, str]):
        manufacturer_url (Union[Unset, str]):
        model_name (Union[Unset, str]):
        model_description (Union[Unset, str]):
        model_number (Union[Unset, str]):
        model_url (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        enable_album_art_in_didl (Union[Unset, bool]):
        enable_single_album_art_limit (Union[Unset, bool]):
        enable_single_subtitle_limit (Union[Unset, bool]):
        protocol_info (Union[Unset, str]):
        timeline_offset_seconds (Union[Unset, int]):
        requires_plain_video_items (Union[Unset, bool]):
        requires_plain_folders (Union[Unset, bool]):
        ignore_transcode_byte_range_requests (Union[Unset, bool]):
        supports_samsung_bookmark (Union[Unset, bool]):
        identification (Union[Unset, EmbyDlnaProfilesDeviceIdentification]):
        protocol_info_detection (Union[Unset, EmbyDlnaProfilesProtocolInfoDetection]):
        name (Union[Unset, str]):
        id (Union[Unset, str]):
        supported_media_types (Union[Unset, str]):
        max_streaming_bitrate (Union[Unset, None, int]):
        music_streaming_transcoding_bitrate (Union[Unset, None, int]):
        max_static_music_bitrate (Union[Unset, None, int]):
        direct_play_profiles (Union[Unset, List['DlnaDirectPlayProfile']]):
        transcoding_profiles (Union[Unset, List['DlnaTranscodingProfile']]):
        container_profiles (Union[Unset, List['DlnaContainerProfile']]):
        codec_profiles (Union[Unset, List['DlnaCodecProfile']]):
        response_profiles (Union[Unset, List['DlnaResponseProfile']]):
        subtitle_profiles (Union[Unset, List['DlnaSubtitleProfile']]):
    """

    type: Union[Unset, EmbyDlnaProfilesDeviceProfileType] = UNSET
    path: Union[Unset, str] = UNSET
    user_id: Union[Unset, str] = UNSET
    album_art_pn: Union[Unset, str] = UNSET
    max_album_art_width: Union[Unset, int] = UNSET
    max_album_art_height: Union[Unset, int] = UNSET
    max_icon_width: Union[Unset, None, int] = UNSET
    max_icon_height: Union[Unset, None, int] = UNSET
    friendly_name: Union[Unset, str] = UNSET
    manufacturer: Union[Unset, str] = UNSET
    manufacturer_url: Union[Unset, str] = UNSET
    model_name: Union[Unset, str] = UNSET
    model_description: Union[Unset, str] = UNSET
    model_number: Union[Unset, str] = UNSET
    model_url: Union[Unset, str] = UNSET
    serial_number: Union[Unset, str] = UNSET
    enable_album_art_in_didl: Union[Unset, bool] = UNSET
    enable_single_album_art_limit: Union[Unset, bool] = UNSET
    enable_single_subtitle_limit: Union[Unset, bool] = UNSET
    protocol_info: Union[Unset, str] = UNSET
    timeline_offset_seconds: Union[Unset, int] = UNSET
    requires_plain_video_items: Union[Unset, bool] = UNSET
    requires_plain_folders: Union[Unset, bool] = UNSET
    ignore_transcode_byte_range_requests: Union[Unset, bool] = UNSET
    supports_samsung_bookmark: Union[Unset, bool] = UNSET
    identification: Union[Unset, "EmbyDlnaProfilesDeviceIdentification"] = UNSET
    protocol_info_detection: Union[Unset, "EmbyDlnaProfilesProtocolInfoDetection"] = UNSET
    name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    supported_media_types: Union[Unset, str] = UNSET
    max_streaming_bitrate: Union[Unset, None, int] = UNSET
    music_streaming_transcoding_bitrate: Union[Unset, None, int] = UNSET
    max_static_music_bitrate: Union[Unset, None, int] = UNSET
    direct_play_profiles: Union[Unset, List["DlnaDirectPlayProfile"]] = UNSET
    transcoding_profiles: Union[Unset, List["DlnaTranscodingProfile"]] = UNSET
    container_profiles: Union[Unset, List["DlnaContainerProfile"]] = UNSET
    codec_profiles: Union[Unset, List["DlnaCodecProfile"]] = UNSET
    response_profiles: Union[Unset, List["DlnaResponseProfile"]] = UNSET
    subtitle_profiles: Union[Unset, List["DlnaSubtitleProfile"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        path = self.path
        user_id = self.user_id
        album_art_pn = self.album_art_pn
        max_album_art_width = self.max_album_art_width
        max_album_art_height = self.max_album_art_height
        max_icon_width = self.max_icon_width
        max_icon_height = self.max_icon_height
        friendly_name = self.friendly_name
        manufacturer = self.manufacturer
        manufacturer_url = self.manufacturer_url
        model_name = self.model_name
        model_description = self.model_description
        model_number = self.model_number
        model_url = self.model_url
        serial_number = self.serial_number
        enable_album_art_in_didl = self.enable_album_art_in_didl
        enable_single_album_art_limit = self.enable_single_album_art_limit
        enable_single_subtitle_limit = self.enable_single_subtitle_limit
        protocol_info = self.protocol_info
        timeline_offset_seconds = self.timeline_offset_seconds
        requires_plain_video_items = self.requires_plain_video_items
        requires_plain_folders = self.requires_plain_folders
        ignore_transcode_byte_range_requests = self.ignore_transcode_byte_range_requests
        supports_samsung_bookmark = self.supports_samsung_bookmark
        identification: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.identification, Unset):
            identification = self.identification.to_dict()

        protocol_info_detection: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.protocol_info_detection, Unset):
            protocol_info_detection = self.protocol_info_detection.to_dict()

        name = self.name
        id = self.id
        supported_media_types = self.supported_media_types
        max_streaming_bitrate = self.max_streaming_bitrate
        music_streaming_transcoding_bitrate = self.music_streaming_transcoding_bitrate
        max_static_music_bitrate = self.max_static_music_bitrate
        direct_play_profiles: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.direct_play_profiles, Unset):
            direct_play_profiles = []
            for direct_play_profiles_item_data in self.direct_play_profiles:
                direct_play_profiles_item = direct_play_profiles_item_data.to_dict()

                direct_play_profiles.append(direct_play_profiles_item)

        transcoding_profiles: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.transcoding_profiles, Unset):
            transcoding_profiles = []
            for transcoding_profiles_item_data in self.transcoding_profiles:
                transcoding_profiles_item = transcoding_profiles_item_data.to_dict()

                transcoding_profiles.append(transcoding_profiles_item)

        container_profiles: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.container_profiles, Unset):
            container_profiles = []
            for container_profiles_item_data in self.container_profiles:
                container_profiles_item = container_profiles_item_data.to_dict()

                container_profiles.append(container_profiles_item)

        codec_profiles: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.codec_profiles, Unset):
            codec_profiles = []
            for codec_profiles_item_data in self.codec_profiles:
                codec_profiles_item = codec_profiles_item_data.to_dict()

                codec_profiles.append(codec_profiles_item)

        response_profiles: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.response_profiles, Unset):
            response_profiles = []
            for response_profiles_item_data in self.response_profiles:
                response_profiles_item = response_profiles_item_data.to_dict()

                response_profiles.append(response_profiles_item)

        subtitle_profiles: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.subtitle_profiles, Unset):
            subtitle_profiles = []
            for subtitle_profiles_item_data in self.subtitle_profiles:
                subtitle_profiles_item = subtitle_profiles_item_data.to_dict()

                subtitle_profiles.append(subtitle_profiles_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["Type"] = type
        if path is not UNSET:
            field_dict["Path"] = path
        if user_id is not UNSET:
            field_dict["UserId"] = user_id
        if album_art_pn is not UNSET:
            field_dict["AlbumArtPn"] = album_art_pn
        if max_album_art_width is not UNSET:
            field_dict["MaxAlbumArtWidth"] = max_album_art_width
        if max_album_art_height is not UNSET:
            field_dict["MaxAlbumArtHeight"] = max_album_art_height
        if max_icon_width is not UNSET:
            field_dict["MaxIconWidth"] = max_icon_width
        if max_icon_height is not UNSET:
            field_dict["MaxIconHeight"] = max_icon_height
        if friendly_name is not UNSET:
            field_dict["FriendlyName"] = friendly_name
        if manufacturer is not UNSET:
            field_dict["Manufacturer"] = manufacturer
        if manufacturer_url is not UNSET:
            field_dict["ManufacturerUrl"] = manufacturer_url
        if model_name is not UNSET:
            field_dict["ModelName"] = model_name
        if model_description is not UNSET:
            field_dict["ModelDescription"] = model_description
        if model_number is not UNSET:
            field_dict["ModelNumber"] = model_number
        if model_url is not UNSET:
            field_dict["ModelUrl"] = model_url
        if serial_number is not UNSET:
            field_dict["SerialNumber"] = serial_number
        if enable_album_art_in_didl is not UNSET:
            field_dict["EnableAlbumArtInDidl"] = enable_album_art_in_didl
        if enable_single_album_art_limit is not UNSET:
            field_dict["EnableSingleAlbumArtLimit"] = enable_single_album_art_limit
        if enable_single_subtitle_limit is not UNSET:
            field_dict["EnableSingleSubtitleLimit"] = enable_single_subtitle_limit
        if protocol_info is not UNSET:
            field_dict["ProtocolInfo"] = protocol_info
        if timeline_offset_seconds is not UNSET:
            field_dict["TimelineOffsetSeconds"] = timeline_offset_seconds
        if requires_plain_video_items is not UNSET:
            field_dict["RequiresPlainVideoItems"] = requires_plain_video_items
        if requires_plain_folders is not UNSET:
            field_dict["RequiresPlainFolders"] = requires_plain_folders
        if ignore_transcode_byte_range_requests is not UNSET:
            field_dict["IgnoreTranscodeByteRangeRequests"] = ignore_transcode_byte_range_requests
        if supports_samsung_bookmark is not UNSET:
            field_dict["SupportsSamsungBookmark"] = supports_samsung_bookmark
        if identification is not UNSET:
            field_dict["Identification"] = identification
        if protocol_info_detection is not UNSET:
            field_dict["ProtocolInfoDetection"] = protocol_info_detection
        if name is not UNSET:
            field_dict["Name"] = name
        if id is not UNSET:
            field_dict["Id"] = id
        if supported_media_types is not UNSET:
            field_dict["SupportedMediaTypes"] = supported_media_types
        if max_streaming_bitrate is not UNSET:
            field_dict["MaxStreamingBitrate"] = max_streaming_bitrate
        if music_streaming_transcoding_bitrate is not UNSET:
            field_dict["MusicStreamingTranscodingBitrate"] = music_streaming_transcoding_bitrate
        if max_static_music_bitrate is not UNSET:
            field_dict["MaxStaticMusicBitrate"] = max_static_music_bitrate
        if direct_play_profiles is not UNSET:
            field_dict["DirectPlayProfiles"] = direct_play_profiles
        if transcoding_profiles is not UNSET:
            field_dict["TranscodingProfiles"] = transcoding_profiles
        if container_profiles is not UNSET:
            field_dict["ContainerProfiles"] = container_profiles
        if codec_profiles is not UNSET:
            field_dict["CodecProfiles"] = codec_profiles
        if response_profiles is not UNSET:
            field_dict["ResponseProfiles"] = response_profiles
        if subtitle_profiles is not UNSET:
            field_dict["SubtitleProfiles"] = subtitle_profiles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dlna_codec_profile import DlnaCodecProfile
        from ..models.dlna_container_profile import DlnaContainerProfile
        from ..models.dlna_direct_play_profile import DlnaDirectPlayProfile
        from ..models.dlna_response_profile import DlnaResponseProfile
        from ..models.dlna_subtitle_profile import DlnaSubtitleProfile
        from ..models.dlna_transcoding_profile import DlnaTranscodingProfile
        from ..models.emby_dlna_profiles_device_identification import EmbyDlnaProfilesDeviceIdentification
        from ..models.emby_dlna_profiles_protocol_info_detection import EmbyDlnaProfilesProtocolInfoDetection

        d = src_dict.copy()
        _type = d.pop("Type", UNSET)
        type: Union[Unset, EmbyDlnaProfilesDeviceProfileType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = EmbyDlnaProfilesDeviceProfileType(_type)

        path = d.pop("Path", UNSET)

        user_id = d.pop("UserId", UNSET)

        album_art_pn = d.pop("AlbumArtPn", UNSET)

        max_album_art_width = d.pop("MaxAlbumArtWidth", UNSET)

        max_album_art_height = d.pop("MaxAlbumArtHeight", UNSET)

        max_icon_width = d.pop("MaxIconWidth", UNSET)

        max_icon_height = d.pop("MaxIconHeight", UNSET)

        friendly_name = d.pop("FriendlyName", UNSET)

        manufacturer = d.pop("Manufacturer", UNSET)

        manufacturer_url = d.pop("ManufacturerUrl", UNSET)

        model_name = d.pop("ModelName", UNSET)

        model_description = d.pop("ModelDescription", UNSET)

        model_number = d.pop("ModelNumber", UNSET)

        model_url = d.pop("ModelUrl", UNSET)

        serial_number = d.pop("SerialNumber", UNSET)

        enable_album_art_in_didl = d.pop("EnableAlbumArtInDidl", UNSET)

        enable_single_album_art_limit = d.pop("EnableSingleAlbumArtLimit", UNSET)

        enable_single_subtitle_limit = d.pop("EnableSingleSubtitleLimit", UNSET)

        protocol_info = d.pop("ProtocolInfo", UNSET)

        timeline_offset_seconds = d.pop("TimelineOffsetSeconds", UNSET)

        requires_plain_video_items = d.pop("RequiresPlainVideoItems", UNSET)

        requires_plain_folders = d.pop("RequiresPlainFolders", UNSET)

        ignore_transcode_byte_range_requests = d.pop("IgnoreTranscodeByteRangeRequests", UNSET)

        supports_samsung_bookmark = d.pop("SupportsSamsungBookmark", UNSET)

        _identification = d.pop("Identification", UNSET)
        identification: Union[Unset, EmbyDlnaProfilesDeviceIdentification]
        if isinstance(_identification, Unset):
            identification = UNSET
        else:
            identification = EmbyDlnaProfilesDeviceIdentification.from_dict(_identification)

        _protocol_info_detection = d.pop("ProtocolInfoDetection", UNSET)
        protocol_info_detection: Union[Unset, EmbyDlnaProfilesProtocolInfoDetection]
        if isinstance(_protocol_info_detection, Unset):
            protocol_info_detection = UNSET
        else:
            protocol_info_detection = EmbyDlnaProfilesProtocolInfoDetection.from_dict(_protocol_info_detection)

        name = d.pop("Name", UNSET)

        id = d.pop("Id", UNSET)

        supported_media_types = d.pop("SupportedMediaTypes", UNSET)

        max_streaming_bitrate = d.pop("MaxStreamingBitrate", UNSET)

        music_streaming_transcoding_bitrate = d.pop("MusicStreamingTranscodingBitrate", UNSET)

        max_static_music_bitrate = d.pop("MaxStaticMusicBitrate", UNSET)

        direct_play_profiles = []
        _direct_play_profiles = d.pop("DirectPlayProfiles", UNSET)
        for direct_play_profiles_item_data in _direct_play_profiles or []:
            direct_play_profiles_item = DlnaDirectPlayProfile.from_dict(direct_play_profiles_item_data)

            direct_play_profiles.append(direct_play_profiles_item)

        transcoding_profiles = []
        _transcoding_profiles = d.pop("TranscodingProfiles", UNSET)
        for transcoding_profiles_item_data in _transcoding_profiles or []:
            transcoding_profiles_item = DlnaTranscodingProfile.from_dict(transcoding_profiles_item_data)

            transcoding_profiles.append(transcoding_profiles_item)

        container_profiles = []
        _container_profiles = d.pop("ContainerProfiles", UNSET)
        for container_profiles_item_data in _container_profiles or []:
            container_profiles_item = DlnaContainerProfile.from_dict(container_profiles_item_data)

            container_profiles.append(container_profiles_item)

        codec_profiles = []
        _codec_profiles = d.pop("CodecProfiles", UNSET)
        for codec_profiles_item_data in _codec_profiles or []:
            codec_profiles_item = DlnaCodecProfile.from_dict(codec_profiles_item_data)

            codec_profiles.append(codec_profiles_item)

        response_profiles = []
        _response_profiles = d.pop("ResponseProfiles", UNSET)
        for response_profiles_item_data in _response_profiles or []:
            response_profiles_item = DlnaResponseProfile.from_dict(response_profiles_item_data)

            response_profiles.append(response_profiles_item)

        subtitle_profiles = []
        _subtitle_profiles = d.pop("SubtitleProfiles", UNSET)
        for subtitle_profiles_item_data in _subtitle_profiles or []:
            subtitle_profiles_item = DlnaSubtitleProfile.from_dict(subtitle_profiles_item_data)

            subtitle_profiles.append(subtitle_profiles_item)

        emby_dlna_profiles_dlna_profile = cls(
            type=type,
            path=path,
            user_id=user_id,
            album_art_pn=album_art_pn,
            max_album_art_width=max_album_art_width,
            max_album_art_height=max_album_art_height,
            max_icon_width=max_icon_width,
            max_icon_height=max_icon_height,
            friendly_name=friendly_name,
            manufacturer=manufacturer,
            manufacturer_url=manufacturer_url,
            model_name=model_name,
            model_description=model_description,
            model_number=model_number,
            model_url=model_url,
            serial_number=serial_number,
            enable_album_art_in_didl=enable_album_art_in_didl,
            enable_single_album_art_limit=enable_single_album_art_limit,
            enable_single_subtitle_limit=enable_single_subtitle_limit,
            protocol_info=protocol_info,
            timeline_offset_seconds=timeline_offset_seconds,
            requires_plain_video_items=requires_plain_video_items,
            requires_plain_folders=requires_plain_folders,
            ignore_transcode_byte_range_requests=ignore_transcode_byte_range_requests,
            supports_samsung_bookmark=supports_samsung_bookmark,
            identification=identification,
            protocol_info_detection=protocol_info_detection,
            name=name,
            id=id,
            supported_media_types=supported_media_types,
            max_streaming_bitrate=max_streaming_bitrate,
            music_streaming_transcoding_bitrate=music_streaming_transcoding_bitrate,
            max_static_music_bitrate=max_static_music_bitrate,
            direct_play_profiles=direct_play_profiles,
            transcoding_profiles=transcoding_profiles,
            container_profiles=container_profiles,
            codec_profiles=codec_profiles,
            response_profiles=response_profiles,
            subtitle_profiles=subtitle_profiles,
        )

        emby_dlna_profiles_dlna_profile.additional_properties = d
        return emby_dlna_profiles_dlna_profile

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
