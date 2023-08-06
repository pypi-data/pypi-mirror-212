from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.library_user_copy_options import LibraryUserCopyOptions
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateUserByName")


@attr.s(auto_attribs=True)
class CreateUserByName:
    """
    Attributes:
        name (Union[Unset, str]):
        copy_from_user_id (Union[Unset, str]):
        user_copy_options (Union[Unset, List[LibraryUserCopyOptions]]):
    """

    name: Union[Unset, str] = UNSET
    copy_from_user_id: Union[Unset, str] = UNSET
    user_copy_options: Union[Unset, List[LibraryUserCopyOptions]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        copy_from_user_id = self.copy_from_user_id
        user_copy_options: Union[Unset, List[str]] = UNSET
        if not isinstance(self.user_copy_options, Unset):
            user_copy_options = []
            for user_copy_options_item_data in self.user_copy_options:
                user_copy_options_item = user_copy_options_item_data.value

                user_copy_options.append(user_copy_options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if copy_from_user_id is not UNSET:
            field_dict["CopyFromUserId"] = copy_from_user_id
        if user_copy_options is not UNSET:
            field_dict["UserCopyOptions"] = user_copy_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        copy_from_user_id = d.pop("CopyFromUserId", UNSET)

        user_copy_options = []
        _user_copy_options = d.pop("UserCopyOptions", UNSET)
        for user_copy_options_item_data in _user_copy_options or []:
            user_copy_options_item = LibraryUserCopyOptions(user_copy_options_item_data)

            user_copy_options.append(user_copy_options_item)

        create_user_by_name = cls(
            name=name,
            copy_from_user_id=copy_from_user_id,
            user_copy_options=user_copy_options,
        )

        create_user_by_name.additional_properties = d
        return create_user_by_name

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
