import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.provider_id_dictionary import ProviderIdDictionary


T = TypeVar("T", bound="RemoteSearchResult")


@attr.s(auto_attribs=True)
class RemoteSearchResult:
    """
    Attributes:
        name (Union[Unset, str]):
        provider_ids (Union[Unset, ProviderIdDictionary]):
        production_year (Union[Unset, None, int]):
        index_number (Union[Unset, None, int]):
        index_number_end (Union[Unset, None, int]):
        parent_index_number (Union[Unset, None, int]):
        premiere_date (Union[Unset, None, datetime.datetime]):
        image_url (Union[Unset, str]):
        search_provider_name (Union[Unset, str]):
        game_system (Union[Unset, str]):
        overview (Union[Unset, str]):
        disambiguation_comment (Union[Unset, str]):
        album_artist (Union[Unset, RemoteSearchResult]):
        artists (Union[Unset, List['RemoteSearchResult']]):
    """

    name: Union[Unset, str] = UNSET
    provider_ids: Union[Unset, "ProviderIdDictionary"] = UNSET
    production_year: Union[Unset, None, int] = UNSET
    index_number: Union[Unset, None, int] = UNSET
    index_number_end: Union[Unset, None, int] = UNSET
    parent_index_number: Union[Unset, None, int] = UNSET
    premiere_date: Union[Unset, None, datetime.datetime] = UNSET
    image_url: Union[Unset, str] = UNSET
    search_provider_name: Union[Unset, str] = UNSET
    game_system: Union[Unset, str] = UNSET
    overview: Union[Unset, str] = UNSET
    disambiguation_comment: Union[Unset, str] = UNSET
    album_artist: Union[Unset, "RemoteSearchResult"] = UNSET
    artists: Union[Unset, List["RemoteSearchResult"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        provider_ids: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.provider_ids, Unset):
            provider_ids = self.provider_ids.to_dict()

        production_year = self.production_year
        index_number = self.index_number
        index_number_end = self.index_number_end
        parent_index_number = self.parent_index_number
        premiere_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.premiere_date, Unset):
            premiere_date = self.premiere_date.isoformat() if self.premiere_date else None

        image_url = self.image_url
        search_provider_name = self.search_provider_name
        game_system = self.game_system
        overview = self.overview
        disambiguation_comment = self.disambiguation_comment
        album_artist: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.album_artist, Unset):
            album_artist = self.album_artist.to_dict()

        artists: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.artists, Unset):
            artists = []
            for artists_item_data in self.artists:
                artists_item = artists_item_data.to_dict()

                artists.append(artists_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if provider_ids is not UNSET:
            field_dict["ProviderIds"] = provider_ids
        if production_year is not UNSET:
            field_dict["ProductionYear"] = production_year
        if index_number is not UNSET:
            field_dict["IndexNumber"] = index_number
        if index_number_end is not UNSET:
            field_dict["IndexNumberEnd"] = index_number_end
        if parent_index_number is not UNSET:
            field_dict["ParentIndexNumber"] = parent_index_number
        if premiere_date is not UNSET:
            field_dict["PremiereDate"] = premiere_date
        if image_url is not UNSET:
            field_dict["ImageUrl"] = image_url
        if search_provider_name is not UNSET:
            field_dict["SearchProviderName"] = search_provider_name
        if game_system is not UNSET:
            field_dict["GameSystem"] = game_system
        if overview is not UNSET:
            field_dict["Overview"] = overview
        if disambiguation_comment is not UNSET:
            field_dict["DisambiguationComment"] = disambiguation_comment
        if album_artist is not UNSET:
            field_dict["AlbumArtist"] = album_artist
        if artists is not UNSET:
            field_dict["Artists"] = artists

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.provider_id_dictionary import ProviderIdDictionary

        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        _provider_ids = d.pop("ProviderIds", UNSET)
        provider_ids: Union[Unset, ProviderIdDictionary]
        if isinstance(_provider_ids, Unset):
            provider_ids = UNSET
        else:
            provider_ids = ProviderIdDictionary.from_dict(_provider_ids)

        production_year = d.pop("ProductionYear", UNSET)

        index_number = d.pop("IndexNumber", UNSET)

        index_number_end = d.pop("IndexNumberEnd", UNSET)

        parent_index_number = d.pop("ParentIndexNumber", UNSET)

        _premiere_date = d.pop("PremiereDate", UNSET)
        premiere_date: Union[Unset, None, datetime.datetime]
        if _premiere_date is None:
            premiere_date = None
        elif isinstance(_premiere_date, Unset):
            premiere_date = UNSET
        else:
            premiere_date = isoparse(_premiere_date)

        image_url = d.pop("ImageUrl", UNSET)

        search_provider_name = d.pop("SearchProviderName", UNSET)

        game_system = d.pop("GameSystem", UNSET)

        overview = d.pop("Overview", UNSET)

        disambiguation_comment = d.pop("DisambiguationComment", UNSET)

        _album_artist = d.pop("AlbumArtist", UNSET)
        album_artist: Union[Unset, RemoteSearchResult]
        if isinstance(_album_artist, Unset):
            album_artist = UNSET
        else:
            album_artist = RemoteSearchResult.from_dict(_album_artist)

        artists = []
        _artists = d.pop("Artists", UNSET)
        for artists_item_data in _artists or []:
            artists_item = RemoteSearchResult.from_dict(artists_item_data)

            artists.append(artists_item)

        remote_search_result = cls(
            name=name,
            provider_ids=provider_ids,
            production_year=production_year,
            index_number=index_number,
            index_number_end=index_number_end,
            parent_index_number=parent_index_number,
            premiere_date=premiere_date,
            image_url=image_url,
            search_provider_name=search_provider_name,
            game_system=game_system,
            overview=overview,
            disambiguation_comment=disambiguation_comment,
            album_artist=album_artist,
            artists=artists,
        )

        remote_search_result.additional_properties = d
        return remote_search_result

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
