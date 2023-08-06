from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_item_dto import BaseItemDto


T = TypeVar("T", bound="LiveTVApiEpgRow")


@attr.s(auto_attribs=True)
class LiveTVApiEpgRow:
    """
    Attributes:
        channel (Union[Unset, BaseItemDto]):
        programs (Union[Unset, List['BaseItemDto']]):
    """

    channel: Union[Unset, "BaseItemDto"] = UNSET
    programs: Union[Unset, List["BaseItemDto"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channel: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.channel, Unset):
            channel = self.channel.to_dict()

        programs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.programs, Unset):
            programs = []
            for programs_item_data in self.programs:
                programs_item = programs_item_data.to_dict()

                programs.append(programs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if channel is not UNSET:
            field_dict["Channel"] = channel
        if programs is not UNSET:
            field_dict["Programs"] = programs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.base_item_dto import BaseItemDto

        d = src_dict.copy()
        _channel = d.pop("Channel", UNSET)
        channel: Union[Unset, BaseItemDto]
        if isinstance(_channel, Unset):
            channel = UNSET
        else:
            channel = BaseItemDto.from_dict(_channel)

        programs = []
        _programs = d.pop("Programs", UNSET)
        for programs_item_data in _programs or []:
            programs_item = BaseItemDto.from_dict(programs_item_data)

            programs.append(programs_item)

        live_tv_api_epg_row = cls(
            channel=channel,
            programs=programs,
        )

        live_tv_api_epg_row.additional_properties = d
        return live_tv_api_epg_row

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
