from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.general_command_arguments import GeneralCommandArguments


T = TypeVar("T", bound="GeneralCommand")


@attr.s(auto_attribs=True)
class GeneralCommand:
    """
    Attributes:
        name (Union[Unset, str]):
        controlling_user_id (Union[Unset, str]):
        arguments (Union[Unset, GeneralCommandArguments]):
    """

    name: Union[Unset, str] = UNSET
    controlling_user_id: Union[Unset, str] = UNSET
    arguments: Union[Unset, "GeneralCommandArguments"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        controlling_user_id = self.controlling_user_id
        arguments: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.arguments, Unset):
            arguments = self.arguments.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if controlling_user_id is not UNSET:
            field_dict["ControllingUserId"] = controlling_user_id
        if arguments is not UNSET:
            field_dict["Arguments"] = arguments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.general_command_arguments import GeneralCommandArguments

        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        controlling_user_id = d.pop("ControllingUserId", UNSET)

        _arguments = d.pop("Arguments", UNSET)
        arguments: Union[Unset, GeneralCommandArguments]
        if isinstance(_arguments, Unset):
            arguments = UNSET
        else:
            arguments = GeneralCommandArguments.from_dict(_arguments)

        general_command = cls(
            name=name,
            controlling_user_id=controlling_user_id,
            arguments=arguments,
        )

        general_command.additional_properties = d
        return general_command

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
