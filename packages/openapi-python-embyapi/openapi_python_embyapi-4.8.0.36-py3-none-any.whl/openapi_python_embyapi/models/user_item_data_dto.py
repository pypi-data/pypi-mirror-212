import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserItemDataDto")


@attr.s(auto_attribs=True)
class UserItemDataDto:
    """
    Attributes:
        rating (Union[Unset, None, float]):
        played_percentage (Union[Unset, None, float]):
        unplayed_item_count (Union[Unset, None, int]):
        playback_position_ticks (Union[Unset, int]):
        play_count (Union[Unset, int]):
        is_favorite (Union[Unset, bool]):
        last_played_date (Union[Unset, None, datetime.datetime]):
        played (Union[Unset, bool]):
        key (Union[Unset, str]):
        item_id (Union[Unset, str]):
        server_id (Union[Unset, str]):
    """

    rating: Union[Unset, None, float] = UNSET
    played_percentage: Union[Unset, None, float] = UNSET
    unplayed_item_count: Union[Unset, None, int] = UNSET
    playback_position_ticks: Union[Unset, int] = UNSET
    play_count: Union[Unset, int] = UNSET
    is_favorite: Union[Unset, bool] = UNSET
    last_played_date: Union[Unset, None, datetime.datetime] = UNSET
    played: Union[Unset, bool] = UNSET
    key: Union[Unset, str] = UNSET
    item_id: Union[Unset, str] = UNSET
    server_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        rating = self.rating
        played_percentage = self.played_percentage
        unplayed_item_count = self.unplayed_item_count
        playback_position_ticks = self.playback_position_ticks
        play_count = self.play_count
        is_favorite = self.is_favorite
        last_played_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_played_date, Unset):
            last_played_date = self.last_played_date.isoformat() if self.last_played_date else None

        played = self.played
        key = self.key
        item_id = self.item_id
        server_id = self.server_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rating is not UNSET:
            field_dict["Rating"] = rating
        if played_percentage is not UNSET:
            field_dict["PlayedPercentage"] = played_percentage
        if unplayed_item_count is not UNSET:
            field_dict["UnplayedItemCount"] = unplayed_item_count
        if playback_position_ticks is not UNSET:
            field_dict["PlaybackPositionTicks"] = playback_position_ticks
        if play_count is not UNSET:
            field_dict["PlayCount"] = play_count
        if is_favorite is not UNSET:
            field_dict["IsFavorite"] = is_favorite
        if last_played_date is not UNSET:
            field_dict["LastPlayedDate"] = last_played_date
        if played is not UNSET:
            field_dict["Played"] = played
        if key is not UNSET:
            field_dict["Key"] = key
        if item_id is not UNSET:
            field_dict["ItemId"] = item_id
        if server_id is not UNSET:
            field_dict["ServerId"] = server_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        rating = d.pop("Rating", UNSET)

        played_percentage = d.pop("PlayedPercentage", UNSET)

        unplayed_item_count = d.pop("UnplayedItemCount", UNSET)

        playback_position_ticks = d.pop("PlaybackPositionTicks", UNSET)

        play_count = d.pop("PlayCount", UNSET)

        is_favorite = d.pop("IsFavorite", UNSET)

        _last_played_date = d.pop("LastPlayedDate", UNSET)
        last_played_date: Union[Unset, None, datetime.datetime]
        if _last_played_date is None:
            last_played_date = None
        elif isinstance(_last_played_date, Unset):
            last_played_date = UNSET
        else:
            last_played_date = isoparse(_last_played_date)

        played = d.pop("Played", UNSET)

        key = d.pop("Key", UNSET)

        item_id = d.pop("ItemId", UNSET)

        server_id = d.pop("ServerId", UNSET)

        user_item_data_dto = cls(
            rating=rating,
            played_percentage=played_percentage,
            unplayed_item_count=unplayed_item_count,
            playback_position_ticks=playback_position_ticks,
            play_count=play_count,
            is_favorite=is_favorite,
            last_played_date=last_played_date,
            played=played,
            key=key,
            item_id=item_id,
            server_id=server_id,
        )

        user_item_data_dto.additional_properties = d
        return user_item_data_dto

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
