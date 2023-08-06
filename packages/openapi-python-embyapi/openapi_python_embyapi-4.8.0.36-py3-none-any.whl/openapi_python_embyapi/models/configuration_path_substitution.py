from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConfigurationPathSubstitution")


@attr.s(auto_attribs=True)
class ConfigurationPathSubstitution:
    """
    Attributes:
        from_ (Union[Unset, str]):
        to (Union[Unset, str]):
    """

    from_: Union[Unset, str] = UNSET
    to: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from_ = self.from_
        to = self.to

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if from_ is not UNSET:
            field_dict["From"] = from_
        if to is not UNSET:
            field_dict["To"] = to

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        from_ = d.pop("From", UNSET)

        to = d.pop("To", UNSET)

        configuration_path_substitution = cls(
            from_=from_,
            to=to,
        )

        configuration_path_substitution.additional_properties = d
        return configuration_path_substitution

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
