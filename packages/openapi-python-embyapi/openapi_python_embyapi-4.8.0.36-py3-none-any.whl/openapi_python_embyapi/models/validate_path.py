from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ValidatePath")


@attr.s(auto_attribs=True)
class ValidatePath:
    """
    Attributes:
        validate_writeable (Union[Unset, bool]):
        is_file (Union[Unset, None, bool]):
    """

    validate_writeable: Union[Unset, bool] = UNSET
    is_file: Union[Unset, None, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        validate_writeable = self.validate_writeable
        is_file = self.is_file

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if validate_writeable is not UNSET:
            field_dict["ValidateWriteable"] = validate_writeable
        if is_file is not UNSET:
            field_dict["IsFile"] = is_file

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        validate_writeable = d.pop("ValidateWriteable", UNSET)

        is_file = d.pop("IsFile", UNSET)

        validate_path = cls(
            validate_writeable=validate_writeable,
            is_file=is_file,
        )

        validate_path.additional_properties = d
        return validate_path

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
