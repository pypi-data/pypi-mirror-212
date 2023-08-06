from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_item_dto import BaseItemDto
    from ..models.queue_item import QueueItem


T = TypeVar("T", bound="PlaybackStopInfo")


@attr.s(auto_attribs=True)
class PlaybackStopInfo:
    """
    Attributes:
        now_playing_queue (Union[Unset, List['QueueItem']]):
        playlist_item_id (Union[Unset, str]):
        playlist_index (Union[Unset, int]):
        playlist_length (Union[Unset, int]):
        item (Union[Unset, BaseItemDto]):
        item_id (Union[Unset, str]):
        session_id (Union[Unset, str]):
        media_source_id (Union[Unset, str]):
        position_ticks (Union[Unset, None, int]):
        live_stream_id (Union[Unset, str]):
        play_session_id (Union[Unset, str]):
        failed (Union[Unset, bool]):
        next_media_type (Union[Unset, str]):
    """

    now_playing_queue: Union[Unset, List["QueueItem"]] = UNSET
    playlist_item_id: Union[Unset, str] = UNSET
    playlist_index: Union[Unset, int] = UNSET
    playlist_length: Union[Unset, int] = UNSET
    item: Union[Unset, "BaseItemDto"] = UNSET
    item_id: Union[Unset, str] = UNSET
    session_id: Union[Unset, str] = UNSET
    media_source_id: Union[Unset, str] = UNSET
    position_ticks: Union[Unset, None, int] = UNSET
    live_stream_id: Union[Unset, str] = UNSET
    play_session_id: Union[Unset, str] = UNSET
    failed: Union[Unset, bool] = UNSET
    next_media_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        now_playing_queue: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.now_playing_queue, Unset):
            now_playing_queue = []
            for now_playing_queue_item_data in self.now_playing_queue:
                now_playing_queue_item = now_playing_queue_item_data.to_dict()

                now_playing_queue.append(now_playing_queue_item)

        playlist_item_id = self.playlist_item_id
        playlist_index = self.playlist_index
        playlist_length = self.playlist_length
        item: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.item, Unset):
            item = self.item.to_dict()

        item_id = self.item_id
        session_id = self.session_id
        media_source_id = self.media_source_id
        position_ticks = self.position_ticks
        live_stream_id = self.live_stream_id
        play_session_id = self.play_session_id
        failed = self.failed
        next_media_type = self.next_media_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if now_playing_queue is not UNSET:
            field_dict["NowPlayingQueue"] = now_playing_queue
        if playlist_item_id is not UNSET:
            field_dict["PlaylistItemId"] = playlist_item_id
        if playlist_index is not UNSET:
            field_dict["PlaylistIndex"] = playlist_index
        if playlist_length is not UNSET:
            field_dict["PlaylistLength"] = playlist_length
        if item is not UNSET:
            field_dict["Item"] = item
        if item_id is not UNSET:
            field_dict["ItemId"] = item_id
        if session_id is not UNSET:
            field_dict["SessionId"] = session_id
        if media_source_id is not UNSET:
            field_dict["MediaSourceId"] = media_source_id
        if position_ticks is not UNSET:
            field_dict["PositionTicks"] = position_ticks
        if live_stream_id is not UNSET:
            field_dict["LiveStreamId"] = live_stream_id
        if play_session_id is not UNSET:
            field_dict["PlaySessionId"] = play_session_id
        if failed is not UNSET:
            field_dict["Failed"] = failed
        if next_media_type is not UNSET:
            field_dict["NextMediaType"] = next_media_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.base_item_dto import BaseItemDto
        from ..models.queue_item import QueueItem

        d = src_dict.copy()
        now_playing_queue = []
        _now_playing_queue = d.pop("NowPlayingQueue", UNSET)
        for now_playing_queue_item_data in _now_playing_queue or []:
            now_playing_queue_item = QueueItem.from_dict(now_playing_queue_item_data)

            now_playing_queue.append(now_playing_queue_item)

        playlist_item_id = d.pop("PlaylistItemId", UNSET)

        playlist_index = d.pop("PlaylistIndex", UNSET)

        playlist_length = d.pop("PlaylistLength", UNSET)

        _item = d.pop("Item", UNSET)
        item: Union[Unset, BaseItemDto]
        if isinstance(_item, Unset):
            item = UNSET
        else:
            item = BaseItemDto.from_dict(_item)

        item_id = d.pop("ItemId", UNSET)

        session_id = d.pop("SessionId", UNSET)

        media_source_id = d.pop("MediaSourceId", UNSET)

        position_ticks = d.pop("PositionTicks", UNSET)

        live_stream_id = d.pop("LiveStreamId", UNSET)

        play_session_id = d.pop("PlaySessionId", UNSET)

        failed = d.pop("Failed", UNSET)

        next_media_type = d.pop("NextMediaType", UNSET)

        playback_stop_info = cls(
            now_playing_queue=now_playing_queue,
            playlist_item_id=playlist_item_id,
            playlist_index=playlist_index,
            playlist_length=playlist_length,
            item=item,
            item_id=item_id,
            session_id=session_id,
            media_source_id=media_source_id,
            position_ticks=position_ticks,
            live_stream_id=live_stream_id,
            play_session_id=play_session_id,
            failed=failed,
            next_media_type=next_media_type,
        )

        playback_stop_info.additional_properties = d
        return playback_stop_info

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
