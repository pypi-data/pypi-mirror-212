from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlaylistsAddToPlaylistResult")


@attr.s(auto_attribs=True)
class PlaylistsAddToPlaylistResult:
    """
    Attributes:
        id (Union[Unset, str]):
        item_added_count (Union[Unset, int]):
    """

    id: Union[Unset, str] = UNSET
    item_added_count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        item_added_count = self.item_added_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if item_added_count is not UNSET:
            field_dict["ItemAddedCount"] = item_added_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        item_added_count = d.pop("ItemAddedCount", UNSET)

        playlists_add_to_playlist_result = cls(
            id=id,
            item_added_count=item_added_count,
        )

        playlists_add_to_playlist_result.additional_properties = d
        return playlists_add_to_playlist_result

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
