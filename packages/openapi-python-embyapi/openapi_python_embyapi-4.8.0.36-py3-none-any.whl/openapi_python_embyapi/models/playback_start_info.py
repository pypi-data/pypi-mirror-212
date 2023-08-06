from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.play_method import PlayMethod
from ..models.progress_event import ProgressEvent
from ..models.repeat_mode import RepeatMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_item_dto import BaseItemDto
    from ..models.queue_item import QueueItem


T = TypeVar("T", bound="PlaybackStartInfo")


@attr.s(auto_attribs=True)
class PlaybackStartInfo:
    """
    Attributes:
        can_seek (Union[Unset, bool]):
        item (Union[Unset, BaseItemDto]):
        now_playing_queue (Union[Unset, List['QueueItem']]):
        playlist_item_id (Union[Unset, str]):
        item_id (Union[Unset, str]):
        session_id (Union[Unset, str]):
        media_source_id (Union[Unset, str]):
        audio_stream_index (Union[Unset, None, int]):
        subtitle_stream_index (Union[Unset, None, int]):
        is_paused (Union[Unset, bool]):
        playlist_index (Union[Unset, int]):
        playlist_length (Union[Unset, int]):
        is_muted (Union[Unset, bool]):
        position_ticks (Union[Unset, None, int]):
        run_time_ticks (Union[Unset, None, int]):
        playback_start_time_ticks (Union[Unset, None, int]):
        volume_level (Union[Unset, None, int]):
        brightness (Union[Unset, None, int]):
        aspect_ratio (Union[Unset, str]):
        event_name (Union[Unset, ProgressEvent]):
        play_method (Union[Unset, PlayMethod]):
        live_stream_id (Union[Unset, str]):
        play_session_id (Union[Unset, str]):
        repeat_mode (Union[Unset, RepeatMode]):
        subtitle_offset (Union[Unset, int]):
        playback_rate (Union[Unset, float]):
        playlist_item_ids (Union[Unset, List[str]]):
    """

    can_seek: Union[Unset, bool] = UNSET
    item: Union[Unset, "BaseItemDto"] = UNSET
    now_playing_queue: Union[Unset, List["QueueItem"]] = UNSET
    playlist_item_id: Union[Unset, str] = UNSET
    item_id: Union[Unset, str] = UNSET
    session_id: Union[Unset, str] = UNSET
    media_source_id: Union[Unset, str] = UNSET
    audio_stream_index: Union[Unset, None, int] = UNSET
    subtitle_stream_index: Union[Unset, None, int] = UNSET
    is_paused: Union[Unset, bool] = UNSET
    playlist_index: Union[Unset, int] = UNSET
    playlist_length: Union[Unset, int] = UNSET
    is_muted: Union[Unset, bool] = UNSET
    position_ticks: Union[Unset, None, int] = UNSET
    run_time_ticks: Union[Unset, None, int] = UNSET
    playback_start_time_ticks: Union[Unset, None, int] = UNSET
    volume_level: Union[Unset, None, int] = UNSET
    brightness: Union[Unset, None, int] = UNSET
    aspect_ratio: Union[Unset, str] = UNSET
    event_name: Union[Unset, ProgressEvent] = UNSET
    play_method: Union[Unset, PlayMethod] = UNSET
    live_stream_id: Union[Unset, str] = UNSET
    play_session_id: Union[Unset, str] = UNSET
    repeat_mode: Union[Unset, RepeatMode] = UNSET
    subtitle_offset: Union[Unset, int] = UNSET
    playback_rate: Union[Unset, float] = UNSET
    playlist_item_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        can_seek = self.can_seek
        item: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.item, Unset):
            item = self.item.to_dict()

        now_playing_queue: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.now_playing_queue, Unset):
            now_playing_queue = []
            for now_playing_queue_item_data in self.now_playing_queue:
                now_playing_queue_item = now_playing_queue_item_data.to_dict()

                now_playing_queue.append(now_playing_queue_item)

        playlist_item_id = self.playlist_item_id
        item_id = self.item_id
        session_id = self.session_id
        media_source_id = self.media_source_id
        audio_stream_index = self.audio_stream_index
        subtitle_stream_index = self.subtitle_stream_index
        is_paused = self.is_paused
        playlist_index = self.playlist_index
        playlist_length = self.playlist_length
        is_muted = self.is_muted
        position_ticks = self.position_ticks
        run_time_ticks = self.run_time_ticks
        playback_start_time_ticks = self.playback_start_time_ticks
        volume_level = self.volume_level
        brightness = self.brightness
        aspect_ratio = self.aspect_ratio
        event_name: Union[Unset, str] = UNSET
        if not isinstance(self.event_name, Unset):
            event_name = self.event_name.value

        play_method: Union[Unset, str] = UNSET
        if not isinstance(self.play_method, Unset):
            play_method = self.play_method.value

        live_stream_id = self.live_stream_id
        play_session_id = self.play_session_id
        repeat_mode: Union[Unset, str] = UNSET
        if not isinstance(self.repeat_mode, Unset):
            repeat_mode = self.repeat_mode.value

        subtitle_offset = self.subtitle_offset
        playback_rate = self.playback_rate
        playlist_item_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.playlist_item_ids, Unset):
            playlist_item_ids = self.playlist_item_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if can_seek is not UNSET:
            field_dict["CanSeek"] = can_seek
        if item is not UNSET:
            field_dict["Item"] = item
        if now_playing_queue is not UNSET:
            field_dict["NowPlayingQueue"] = now_playing_queue
        if playlist_item_id is not UNSET:
            field_dict["PlaylistItemId"] = playlist_item_id
        if item_id is not UNSET:
            field_dict["ItemId"] = item_id
        if session_id is not UNSET:
            field_dict["SessionId"] = session_id
        if media_source_id is not UNSET:
            field_dict["MediaSourceId"] = media_source_id
        if audio_stream_index is not UNSET:
            field_dict["AudioStreamIndex"] = audio_stream_index
        if subtitle_stream_index is not UNSET:
            field_dict["SubtitleStreamIndex"] = subtitle_stream_index
        if is_paused is not UNSET:
            field_dict["IsPaused"] = is_paused
        if playlist_index is not UNSET:
            field_dict["PlaylistIndex"] = playlist_index
        if playlist_length is not UNSET:
            field_dict["PlaylistLength"] = playlist_length
        if is_muted is not UNSET:
            field_dict["IsMuted"] = is_muted
        if position_ticks is not UNSET:
            field_dict["PositionTicks"] = position_ticks
        if run_time_ticks is not UNSET:
            field_dict["RunTimeTicks"] = run_time_ticks
        if playback_start_time_ticks is not UNSET:
            field_dict["PlaybackStartTimeTicks"] = playback_start_time_ticks
        if volume_level is not UNSET:
            field_dict["VolumeLevel"] = volume_level
        if brightness is not UNSET:
            field_dict["Brightness"] = brightness
        if aspect_ratio is not UNSET:
            field_dict["AspectRatio"] = aspect_ratio
        if event_name is not UNSET:
            field_dict["EventName"] = event_name
        if play_method is not UNSET:
            field_dict["PlayMethod"] = play_method
        if live_stream_id is not UNSET:
            field_dict["LiveStreamId"] = live_stream_id
        if play_session_id is not UNSET:
            field_dict["PlaySessionId"] = play_session_id
        if repeat_mode is not UNSET:
            field_dict["RepeatMode"] = repeat_mode
        if subtitle_offset is not UNSET:
            field_dict["SubtitleOffset"] = subtitle_offset
        if playback_rate is not UNSET:
            field_dict["PlaybackRate"] = playback_rate
        if playlist_item_ids is not UNSET:
            field_dict["PlaylistItemIds"] = playlist_item_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.base_item_dto import BaseItemDto
        from ..models.queue_item import QueueItem

        d = src_dict.copy()
        can_seek = d.pop("CanSeek", UNSET)

        _item = d.pop("Item", UNSET)
        item: Union[Unset, BaseItemDto]
        if isinstance(_item, Unset):
            item = UNSET
        else:
            item = BaseItemDto.from_dict(_item)

        now_playing_queue = []
        _now_playing_queue = d.pop("NowPlayingQueue", UNSET)
        for now_playing_queue_item_data in _now_playing_queue or []:
            now_playing_queue_item = QueueItem.from_dict(now_playing_queue_item_data)

            now_playing_queue.append(now_playing_queue_item)

        playlist_item_id = d.pop("PlaylistItemId", UNSET)

        item_id = d.pop("ItemId", UNSET)

        session_id = d.pop("SessionId", UNSET)

        media_source_id = d.pop("MediaSourceId", UNSET)

        audio_stream_index = d.pop("AudioStreamIndex", UNSET)

        subtitle_stream_index = d.pop("SubtitleStreamIndex", UNSET)

        is_paused = d.pop("IsPaused", UNSET)

        playlist_index = d.pop("PlaylistIndex", UNSET)

        playlist_length = d.pop("PlaylistLength", UNSET)

        is_muted = d.pop("IsMuted", UNSET)

        position_ticks = d.pop("PositionTicks", UNSET)

        run_time_ticks = d.pop("RunTimeTicks", UNSET)

        playback_start_time_ticks = d.pop("PlaybackStartTimeTicks", UNSET)

        volume_level = d.pop("VolumeLevel", UNSET)

        brightness = d.pop("Brightness", UNSET)

        aspect_ratio = d.pop("AspectRatio", UNSET)

        _event_name = d.pop("EventName", UNSET)
        event_name: Union[Unset, ProgressEvent]
        if isinstance(_event_name, Unset):
            event_name = UNSET
        else:
            event_name = ProgressEvent(_event_name)

        _play_method = d.pop("PlayMethod", UNSET)
        play_method: Union[Unset, PlayMethod]
        if isinstance(_play_method, Unset):
            play_method = UNSET
        else:
            play_method = PlayMethod(_play_method)

        live_stream_id = d.pop("LiveStreamId", UNSET)

        play_session_id = d.pop("PlaySessionId", UNSET)

        _repeat_mode = d.pop("RepeatMode", UNSET)
        repeat_mode: Union[Unset, RepeatMode]
        if isinstance(_repeat_mode, Unset):
            repeat_mode = UNSET
        else:
            repeat_mode = RepeatMode(_repeat_mode)

        subtitle_offset = d.pop("SubtitleOffset", UNSET)

        playback_rate = d.pop("PlaybackRate", UNSET)

        playlist_item_ids = cast(List[str], d.pop("PlaylistItemIds", UNSET))

        playback_start_info = cls(
            can_seek=can_seek,
            item=item,
            now_playing_queue=now_playing_queue,
            playlist_item_id=playlist_item_id,
            item_id=item_id,
            session_id=session_id,
            media_source_id=media_source_id,
            audio_stream_index=audio_stream_index,
            subtitle_stream_index=subtitle_stream_index,
            is_paused=is_paused,
            playlist_index=playlist_index,
            playlist_length=playlist_length,
            is_muted=is_muted,
            position_ticks=position_ticks,
            run_time_ticks=run_time_ticks,
            playback_start_time_ticks=playback_start_time_ticks,
            volume_level=volume_level,
            brightness=brightness,
            aspect_ratio=aspect_ratio,
            event_name=event_name,
            play_method=play_method,
            live_stream_id=live_stream_id,
            play_session_id=play_session_id,
            repeat_mode=repeat_mode,
            subtitle_offset=subtitle_offset,
            playback_rate=playback_rate,
            playlist_item_ids=playlist_item_ids,
        )

        playback_start_info.additional_properties = d
        return playback_start_info

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
