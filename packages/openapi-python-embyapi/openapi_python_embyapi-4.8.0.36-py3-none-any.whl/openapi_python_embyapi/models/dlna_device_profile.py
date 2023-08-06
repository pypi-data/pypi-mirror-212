from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dlna_codec_profile import DlnaCodecProfile
    from ..models.dlna_container_profile import DlnaContainerProfile
    from ..models.dlna_direct_play_profile import DlnaDirectPlayProfile
    from ..models.dlna_response_profile import DlnaResponseProfile
    from ..models.dlna_subtitle_profile import DlnaSubtitleProfile
    from ..models.dlna_transcoding_profile import DlnaTranscodingProfile


T = TypeVar("T", bound="DlnaDeviceProfile")


@attr.s(auto_attribs=True)
class DlnaDeviceProfile:
    """
    Attributes:
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

        d = src_dict.copy()
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

        dlna_device_profile = cls(
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

        dlna_device_profile.additional_properties = d
        return dlna_device_profile

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
