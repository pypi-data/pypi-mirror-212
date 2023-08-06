from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LiveTvTunerHostInfo")


@attr.s(auto_attribs=True)
class LiveTvTunerHostInfo:
    """
    Attributes:
        id (Union[Unset, str]):
        url (Union[Unset, str]):
        type (Union[Unset, str]):
        device_id (Union[Unset, str]):
        friendly_name (Union[Unset, str]):
        setup_url (Union[Unset, str]):
        import_favorites_only (Union[Unset, bool]):
        prefer_epg_channel_images (Union[Unset, bool]):
        prefer_epg_channel_numbers (Union[Unset, bool]):
        allow_hw_transcoding (Union[Unset, bool]):
        allow_mapping_by_number (Union[Unset, bool]):
        source (Union[Unset, str]):
        tuner_count (Union[Unset, int]):
        user_agent (Union[Unset, str]):
        referrer (Union[Unset, str]):
        provider_options (Union[Unset, str]):
        data_version (Union[Unset, int]):
    """

    id: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    device_id: Union[Unset, str] = UNSET
    friendly_name: Union[Unset, str] = UNSET
    setup_url: Union[Unset, str] = UNSET
    import_favorites_only: Union[Unset, bool] = UNSET
    prefer_epg_channel_images: Union[Unset, bool] = UNSET
    prefer_epg_channel_numbers: Union[Unset, bool] = UNSET
    allow_hw_transcoding: Union[Unset, bool] = UNSET
    allow_mapping_by_number: Union[Unset, bool] = UNSET
    source: Union[Unset, str] = UNSET
    tuner_count: Union[Unset, int] = UNSET
    user_agent: Union[Unset, str] = UNSET
    referrer: Union[Unset, str] = UNSET
    provider_options: Union[Unset, str] = UNSET
    data_version: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        url = self.url
        type = self.type
        device_id = self.device_id
        friendly_name = self.friendly_name
        setup_url = self.setup_url
        import_favorites_only = self.import_favorites_only
        prefer_epg_channel_images = self.prefer_epg_channel_images
        prefer_epg_channel_numbers = self.prefer_epg_channel_numbers
        allow_hw_transcoding = self.allow_hw_transcoding
        allow_mapping_by_number = self.allow_mapping_by_number
        source = self.source
        tuner_count = self.tuner_count
        user_agent = self.user_agent
        referrer = self.referrer
        provider_options = self.provider_options
        data_version = self.data_version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if url is not UNSET:
            field_dict["Url"] = url
        if type is not UNSET:
            field_dict["Type"] = type
        if device_id is not UNSET:
            field_dict["DeviceId"] = device_id
        if friendly_name is not UNSET:
            field_dict["FriendlyName"] = friendly_name
        if setup_url is not UNSET:
            field_dict["SetupUrl"] = setup_url
        if import_favorites_only is not UNSET:
            field_dict["ImportFavoritesOnly"] = import_favorites_only
        if prefer_epg_channel_images is not UNSET:
            field_dict["PreferEpgChannelImages"] = prefer_epg_channel_images
        if prefer_epg_channel_numbers is not UNSET:
            field_dict["PreferEpgChannelNumbers"] = prefer_epg_channel_numbers
        if allow_hw_transcoding is not UNSET:
            field_dict["AllowHWTranscoding"] = allow_hw_transcoding
        if allow_mapping_by_number is not UNSET:
            field_dict["AllowMappingByNumber"] = allow_mapping_by_number
        if source is not UNSET:
            field_dict["Source"] = source
        if tuner_count is not UNSET:
            field_dict["TunerCount"] = tuner_count
        if user_agent is not UNSET:
            field_dict["UserAgent"] = user_agent
        if referrer is not UNSET:
            field_dict["Referrer"] = referrer
        if provider_options is not UNSET:
            field_dict["ProviderOptions"] = provider_options
        if data_version is not UNSET:
            field_dict["DataVersion"] = data_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        url = d.pop("Url", UNSET)

        type = d.pop("Type", UNSET)

        device_id = d.pop("DeviceId", UNSET)

        friendly_name = d.pop("FriendlyName", UNSET)

        setup_url = d.pop("SetupUrl", UNSET)

        import_favorites_only = d.pop("ImportFavoritesOnly", UNSET)

        prefer_epg_channel_images = d.pop("PreferEpgChannelImages", UNSET)

        prefer_epg_channel_numbers = d.pop("PreferEpgChannelNumbers", UNSET)

        allow_hw_transcoding = d.pop("AllowHWTranscoding", UNSET)

        allow_mapping_by_number = d.pop("AllowMappingByNumber", UNSET)

        source = d.pop("Source", UNSET)

        tuner_count = d.pop("TunerCount", UNSET)

        user_agent = d.pop("UserAgent", UNSET)

        referrer = d.pop("Referrer", UNSET)

        provider_options = d.pop("ProviderOptions", UNSET)

        data_version = d.pop("DataVersion", UNSET)

        live_tv_tuner_host_info = cls(
            id=id,
            url=url,
            type=type,
            device_id=device_id,
            friendly_name=friendly_name,
            setup_url=setup_url,
            import_favorites_only=import_favorites_only,
            prefer_epg_channel_images=prefer_epg_channel_images,
            prefer_epg_channel_numbers=prefer_epg_channel_numbers,
            allow_hw_transcoding=allow_hw_transcoding,
            allow_mapping_by_number=allow_mapping_by_number,
            source=source,
            tuner_count=tuner_count,
            user_agent=user_agent,
            referrer=referrer,
            provider_options=provider_options,
            data_version=data_version,
        )

        live_tv_tuner_host_info.additional_properties = d
        return live_tv_tuner_host_info

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
