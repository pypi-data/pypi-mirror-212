import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_item_dto import BaseItemDto
    from ..models.player_state_info import PlayerStateInfo
    from ..models.session_user_info import SessionUserInfo
    from ..models.transcoding_info import TranscodingInfo


T = TypeVar("T", bound="SessionSessionInfo")


@attr.s(auto_attribs=True)
class SessionSessionInfo:
    """
    Attributes:
        play_state (Union[Unset, PlayerStateInfo]):
        additional_users (Union[Unset, List['SessionUserInfo']]):
        remote_end_point (Union[Unset, str]):
        protocol (Union[Unset, str]):
        playable_media_types (Union[Unset, List[str]]):
        playlist_item_id (Union[Unset, str]):
        playlist_index (Union[Unset, int]):
        playlist_length (Union[Unset, int]):
        id (Union[Unset, str]):
        server_id (Union[Unset, str]):
        user_id (Union[Unset, str]):
        user_name (Union[Unset, str]):
        user_primary_image_tag (Union[Unset, str]):
        client (Union[Unset, str]):
        last_activity_date (Union[Unset, datetime.datetime]):
        device_name (Union[Unset, str]):
        device_type (Union[Unset, str]):
        now_playing_item (Union[Unset, BaseItemDto]):
        internal_device_id (Union[Unset, int]):
        device_id (Union[Unset, str]):
        application_version (Union[Unset, str]):
        app_icon_url (Union[Unset, str]):
        supported_commands (Union[Unset, List[str]]):
        transcoding_info (Union[Unset, TranscodingInfo]):
        supports_remote_control (Union[Unset, bool]):
    """

    play_state: Union[Unset, "PlayerStateInfo"] = UNSET
    additional_users: Union[Unset, List["SessionUserInfo"]] = UNSET
    remote_end_point: Union[Unset, str] = UNSET
    protocol: Union[Unset, str] = UNSET
    playable_media_types: Union[Unset, List[str]] = UNSET
    playlist_item_id: Union[Unset, str] = UNSET
    playlist_index: Union[Unset, int] = UNSET
    playlist_length: Union[Unset, int] = UNSET
    id: Union[Unset, str] = UNSET
    server_id: Union[Unset, str] = UNSET
    user_id: Union[Unset, str] = UNSET
    user_name: Union[Unset, str] = UNSET
    user_primary_image_tag: Union[Unset, str] = UNSET
    client: Union[Unset, str] = UNSET
    last_activity_date: Union[Unset, datetime.datetime] = UNSET
    device_name: Union[Unset, str] = UNSET
    device_type: Union[Unset, str] = UNSET
    now_playing_item: Union[Unset, "BaseItemDto"] = UNSET
    internal_device_id: Union[Unset, int] = UNSET
    device_id: Union[Unset, str] = UNSET
    application_version: Union[Unset, str] = UNSET
    app_icon_url: Union[Unset, str] = UNSET
    supported_commands: Union[Unset, List[str]] = UNSET
    transcoding_info: Union[Unset, "TranscodingInfo"] = UNSET
    supports_remote_control: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        play_state: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.play_state, Unset):
            play_state = self.play_state.to_dict()

        additional_users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.additional_users, Unset):
            additional_users = []
            for additional_users_item_data in self.additional_users:
                additional_users_item = additional_users_item_data.to_dict()

                additional_users.append(additional_users_item)

        remote_end_point = self.remote_end_point
        protocol = self.protocol
        playable_media_types: Union[Unset, List[str]] = UNSET
        if not isinstance(self.playable_media_types, Unset):
            playable_media_types = self.playable_media_types

        playlist_item_id = self.playlist_item_id
        playlist_index = self.playlist_index
        playlist_length = self.playlist_length
        id = self.id
        server_id = self.server_id
        user_id = self.user_id
        user_name = self.user_name
        user_primary_image_tag = self.user_primary_image_tag
        client = self.client
        last_activity_date: Union[Unset, str] = UNSET
        if not isinstance(self.last_activity_date, Unset):
            last_activity_date = self.last_activity_date.isoformat()

        device_name = self.device_name
        device_type = self.device_type
        now_playing_item: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.now_playing_item, Unset):
            now_playing_item = self.now_playing_item.to_dict()

        internal_device_id = self.internal_device_id
        device_id = self.device_id
        application_version = self.application_version
        app_icon_url = self.app_icon_url
        supported_commands: Union[Unset, List[str]] = UNSET
        if not isinstance(self.supported_commands, Unset):
            supported_commands = self.supported_commands

        transcoding_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.transcoding_info, Unset):
            transcoding_info = self.transcoding_info.to_dict()

        supports_remote_control = self.supports_remote_control

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if play_state is not UNSET:
            field_dict["PlayState"] = play_state
        if additional_users is not UNSET:
            field_dict["AdditionalUsers"] = additional_users
        if remote_end_point is not UNSET:
            field_dict["RemoteEndPoint"] = remote_end_point
        if protocol is not UNSET:
            field_dict["Protocol"] = protocol
        if playable_media_types is not UNSET:
            field_dict["PlayableMediaTypes"] = playable_media_types
        if playlist_item_id is not UNSET:
            field_dict["PlaylistItemId"] = playlist_item_id
        if playlist_index is not UNSET:
            field_dict["PlaylistIndex"] = playlist_index
        if playlist_length is not UNSET:
            field_dict["PlaylistLength"] = playlist_length
        if id is not UNSET:
            field_dict["Id"] = id
        if server_id is not UNSET:
            field_dict["ServerId"] = server_id
        if user_id is not UNSET:
            field_dict["UserId"] = user_id
        if user_name is not UNSET:
            field_dict["UserName"] = user_name
        if user_primary_image_tag is not UNSET:
            field_dict["UserPrimaryImageTag"] = user_primary_image_tag
        if client is not UNSET:
            field_dict["Client"] = client
        if last_activity_date is not UNSET:
            field_dict["LastActivityDate"] = last_activity_date
        if device_name is not UNSET:
            field_dict["DeviceName"] = device_name
        if device_type is not UNSET:
            field_dict["DeviceType"] = device_type
        if now_playing_item is not UNSET:
            field_dict["NowPlayingItem"] = now_playing_item
        if internal_device_id is not UNSET:
            field_dict["InternalDeviceId"] = internal_device_id
        if device_id is not UNSET:
            field_dict["DeviceId"] = device_id
        if application_version is not UNSET:
            field_dict["ApplicationVersion"] = application_version
        if app_icon_url is not UNSET:
            field_dict["AppIconUrl"] = app_icon_url
        if supported_commands is not UNSET:
            field_dict["SupportedCommands"] = supported_commands
        if transcoding_info is not UNSET:
            field_dict["TranscodingInfo"] = transcoding_info
        if supports_remote_control is not UNSET:
            field_dict["SupportsRemoteControl"] = supports_remote_control

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.base_item_dto import BaseItemDto
        from ..models.player_state_info import PlayerStateInfo
        from ..models.session_user_info import SessionUserInfo
        from ..models.transcoding_info import TranscodingInfo

        d = src_dict.copy()
        _play_state = d.pop("PlayState", UNSET)
        play_state: Union[Unset, PlayerStateInfo]
        if isinstance(_play_state, Unset):
            play_state = UNSET
        else:
            play_state = PlayerStateInfo.from_dict(_play_state)

        additional_users = []
        _additional_users = d.pop("AdditionalUsers", UNSET)
        for additional_users_item_data in _additional_users or []:
            additional_users_item = SessionUserInfo.from_dict(additional_users_item_data)

            additional_users.append(additional_users_item)

        remote_end_point = d.pop("RemoteEndPoint", UNSET)

        protocol = d.pop("Protocol", UNSET)

        playable_media_types = cast(List[str], d.pop("PlayableMediaTypes", UNSET))

        playlist_item_id = d.pop("PlaylistItemId", UNSET)

        playlist_index = d.pop("PlaylistIndex", UNSET)

        playlist_length = d.pop("PlaylistLength", UNSET)

        id = d.pop("Id", UNSET)

        server_id = d.pop("ServerId", UNSET)

        user_id = d.pop("UserId", UNSET)

        user_name = d.pop("UserName", UNSET)

        user_primary_image_tag = d.pop("UserPrimaryImageTag", UNSET)

        client = d.pop("Client", UNSET)

        _last_activity_date = d.pop("LastActivityDate", UNSET)
        last_activity_date: Union[Unset, datetime.datetime]
        if isinstance(_last_activity_date, Unset):
            last_activity_date = UNSET
        else:
            last_activity_date = isoparse(_last_activity_date)

        device_name = d.pop("DeviceName", UNSET)

        device_type = d.pop("DeviceType", UNSET)

        _now_playing_item = d.pop("NowPlayingItem", UNSET)
        now_playing_item: Union[Unset, BaseItemDto]
        if isinstance(_now_playing_item, Unset):
            now_playing_item = UNSET
        else:
            now_playing_item = BaseItemDto.from_dict(_now_playing_item)

        internal_device_id = d.pop("InternalDeviceId", UNSET)

        device_id = d.pop("DeviceId", UNSET)

        application_version = d.pop("ApplicationVersion", UNSET)

        app_icon_url = d.pop("AppIconUrl", UNSET)

        supported_commands = cast(List[str], d.pop("SupportedCommands", UNSET))

        _transcoding_info = d.pop("TranscodingInfo", UNSET)
        transcoding_info: Union[Unset, TranscodingInfo]
        if isinstance(_transcoding_info, Unset):
            transcoding_info = UNSET
        else:
            transcoding_info = TranscodingInfo.from_dict(_transcoding_info)

        supports_remote_control = d.pop("SupportsRemoteControl", UNSET)

        session_session_info = cls(
            play_state=play_state,
            additional_users=additional_users,
            remote_end_point=remote_end_point,
            protocol=protocol,
            playable_media_types=playable_media_types,
            playlist_item_id=playlist_item_id,
            playlist_index=playlist_index,
            playlist_length=playlist_length,
            id=id,
            server_id=server_id,
            user_id=user_id,
            user_name=user_name,
            user_primary_image_tag=user_primary_image_tag,
            client=client,
            last_activity_date=last_activity_date,
            device_name=device_name,
            device_type=device_type,
            now_playing_item=now_playing_item,
            internal_device_id=internal_device_id,
            device_id=device_id,
            application_version=application_version,
            app_icon_url=app_icon_url,
            supported_commands=supported_commands,
            transcoding_info=transcoding_info,
            supports_remote_control=supports_remote_control,
        )

        session_session_info.additional_properties = d
        return session_session_info

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
