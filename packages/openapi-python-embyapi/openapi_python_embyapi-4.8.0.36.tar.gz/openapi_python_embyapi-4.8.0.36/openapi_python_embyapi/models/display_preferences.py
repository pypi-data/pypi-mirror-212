from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.sort_order import SortOrder
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.display_preferences_custom_prefs import DisplayPreferencesCustomPrefs


T = TypeVar("T", bound="DisplayPreferences")


@attr.s(auto_attribs=True)
class DisplayPreferences:
    """
    Attributes:
        id (Union[Unset, str]):
        sort_by (Union[Unset, str]):
        custom_prefs (Union[Unset, DisplayPreferencesCustomPrefs]):
        sort_order (Union[Unset, SortOrder]):
        client (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    sort_by: Union[Unset, str] = UNSET
    custom_prefs: Union[Unset, "DisplayPreferencesCustomPrefs"] = UNSET
    sort_order: Union[Unset, SortOrder] = UNSET
    client: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        sort_by = self.sort_by
        custom_prefs: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.custom_prefs, Unset):
            custom_prefs = self.custom_prefs.to_dict()

        sort_order: Union[Unset, str] = UNSET
        if not isinstance(self.sort_order, Unset):
            sort_order = self.sort_order.value

        client = self.client

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["Id"] = id
        if sort_by is not UNSET:
            field_dict["SortBy"] = sort_by
        if custom_prefs is not UNSET:
            field_dict["CustomPrefs"] = custom_prefs
        if sort_order is not UNSET:
            field_dict["SortOrder"] = sort_order
        if client is not UNSET:
            field_dict["Client"] = client

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.display_preferences_custom_prefs import DisplayPreferencesCustomPrefs

        d = src_dict.copy()
        id = d.pop("Id", UNSET)

        sort_by = d.pop("SortBy", UNSET)

        _custom_prefs = d.pop("CustomPrefs", UNSET)
        custom_prefs: Union[Unset, DisplayPreferencesCustomPrefs]
        if isinstance(_custom_prefs, Unset):
            custom_prefs = UNSET
        else:
            custom_prefs = DisplayPreferencesCustomPrefs.from_dict(_custom_prefs)

        _sort_order = d.pop("SortOrder", UNSET)
        sort_order: Union[Unset, SortOrder]
        if isinstance(_sort_order, Unset):
            sort_order = UNSET
        else:
            sort_order = SortOrder(_sort_order)

        client = d.pop("Client", UNSET)

        display_preferences = cls(
            id=id,
            sort_by=sort_by,
            custom_prefs=custom_prefs,
            sort_order=sort_order,
            client=client,
        )

        display_preferences.additional_properties = d
        return display_preferences

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
