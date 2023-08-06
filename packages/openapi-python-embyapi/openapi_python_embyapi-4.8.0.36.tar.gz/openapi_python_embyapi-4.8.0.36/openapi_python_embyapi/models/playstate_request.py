from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.playstate_command import PlaystateCommand
from ..types import UNSET, Unset

T = TypeVar("T", bound="PlaystateRequest")


@attr.s(auto_attribs=True)
class PlaystateRequest:
    """
    Attributes:
        command (Union[Unset, PlaystateCommand]):
        seek_position_ticks (Union[Unset, None, int]):
        controlling_user_id (Union[Unset, str]):
    """

    command: Union[Unset, PlaystateCommand] = UNSET
    seek_position_ticks: Union[Unset, None, int] = UNSET
    controlling_user_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command: Union[Unset, str] = UNSET
        if not isinstance(self.command, Unset):
            command = self.command.value

        seek_position_ticks = self.seek_position_ticks
        controlling_user_id = self.controlling_user_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if command is not UNSET:
            field_dict["Command"] = command
        if seek_position_ticks is not UNSET:
            field_dict["SeekPositionTicks"] = seek_position_ticks
        if controlling_user_id is not UNSET:
            field_dict["ControllingUserId"] = controlling_user_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _command = d.pop("Command", UNSET)
        command: Union[Unset, PlaystateCommand]
        if isinstance(_command, Unset):
            command = UNSET
        else:
            command = PlaystateCommand(_command)

        seek_position_ticks = d.pop("SeekPositionTicks", UNSET)

        controlling_user_id = d.pop("ControllingUserId", UNSET)

        playstate_request = cls(
            command=command,
            seek_position_ticks=seek_position_ticks,
            controlling_user_id=controlling_user_id,
        )

        playstate_request.additional_properties = d
        return playstate_request

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
