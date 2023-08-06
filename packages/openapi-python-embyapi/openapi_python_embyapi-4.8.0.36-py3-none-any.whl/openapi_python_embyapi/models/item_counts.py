from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ItemCounts")


@attr.s(auto_attribs=True)
class ItemCounts:
    """
    Attributes:
        movie_count (Union[Unset, int]):
        series_count (Union[Unset, int]):
        episode_count (Union[Unset, int]):
        game_count (Union[Unset, int]):
        artist_count (Union[Unset, int]):
        program_count (Union[Unset, int]):
        game_system_count (Union[Unset, int]):
        trailer_count (Union[Unset, int]):
        song_count (Union[Unset, int]):
        album_count (Union[Unset, int]):
        music_video_count (Union[Unset, int]):
        box_set_count (Union[Unset, int]):
        book_count (Union[Unset, int]):
        item_count (Union[Unset, int]):
    """

    movie_count: Union[Unset, int] = UNSET
    series_count: Union[Unset, int] = UNSET
    episode_count: Union[Unset, int] = UNSET
    game_count: Union[Unset, int] = UNSET
    artist_count: Union[Unset, int] = UNSET
    program_count: Union[Unset, int] = UNSET
    game_system_count: Union[Unset, int] = UNSET
    trailer_count: Union[Unset, int] = UNSET
    song_count: Union[Unset, int] = UNSET
    album_count: Union[Unset, int] = UNSET
    music_video_count: Union[Unset, int] = UNSET
    box_set_count: Union[Unset, int] = UNSET
    book_count: Union[Unset, int] = UNSET
    item_count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        movie_count = self.movie_count
        series_count = self.series_count
        episode_count = self.episode_count
        game_count = self.game_count
        artist_count = self.artist_count
        program_count = self.program_count
        game_system_count = self.game_system_count
        trailer_count = self.trailer_count
        song_count = self.song_count
        album_count = self.album_count
        music_video_count = self.music_video_count
        box_set_count = self.box_set_count
        book_count = self.book_count
        item_count = self.item_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if movie_count is not UNSET:
            field_dict["MovieCount"] = movie_count
        if series_count is not UNSET:
            field_dict["SeriesCount"] = series_count
        if episode_count is not UNSET:
            field_dict["EpisodeCount"] = episode_count
        if game_count is not UNSET:
            field_dict["GameCount"] = game_count
        if artist_count is not UNSET:
            field_dict["ArtistCount"] = artist_count
        if program_count is not UNSET:
            field_dict["ProgramCount"] = program_count
        if game_system_count is not UNSET:
            field_dict["GameSystemCount"] = game_system_count
        if trailer_count is not UNSET:
            field_dict["TrailerCount"] = trailer_count
        if song_count is not UNSET:
            field_dict["SongCount"] = song_count
        if album_count is not UNSET:
            field_dict["AlbumCount"] = album_count
        if music_video_count is not UNSET:
            field_dict["MusicVideoCount"] = music_video_count
        if box_set_count is not UNSET:
            field_dict["BoxSetCount"] = box_set_count
        if book_count is not UNSET:
            field_dict["BookCount"] = book_count
        if item_count is not UNSET:
            field_dict["ItemCount"] = item_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        movie_count = d.pop("MovieCount", UNSET)

        series_count = d.pop("SeriesCount", UNSET)

        episode_count = d.pop("EpisodeCount", UNSET)

        game_count = d.pop("GameCount", UNSET)

        artist_count = d.pop("ArtistCount", UNSET)

        program_count = d.pop("ProgramCount", UNSET)

        game_system_count = d.pop("GameSystemCount", UNSET)

        trailer_count = d.pop("TrailerCount", UNSET)

        song_count = d.pop("SongCount", UNSET)

        album_count = d.pop("AlbumCount", UNSET)

        music_video_count = d.pop("MusicVideoCount", UNSET)

        box_set_count = d.pop("BoxSetCount", UNSET)

        book_count = d.pop("BookCount", UNSET)

        item_count = d.pop("ItemCount", UNSET)

        item_counts = cls(
            movie_count=movie_count,
            series_count=series_count,
            episode_count=episode_count,
            game_count=game_count,
            artist_count=artist_count,
            program_count=program_count,
            game_system_count=game_system_count,
            trailer_count=trailer_count,
            song_count=song_count,
            album_count=album_count,
            music_video_count=music_video_count,
            box_set_count=box_set_count,
            book_count=book_count,
            item_count=item_count,
        )

        item_counts.additional_properties = d
        return item_counts

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
