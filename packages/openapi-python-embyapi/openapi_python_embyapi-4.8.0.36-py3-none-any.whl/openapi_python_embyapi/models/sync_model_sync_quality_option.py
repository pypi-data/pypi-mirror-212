from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SyncModelSyncQualityOption")


@attr.s(auto_attribs=True)
class SyncModelSyncQualityOption:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        id (Union[Unset, str]):
        is_default (Union[Unset, bool]):
        is_original_quality (Union[Unset, bool]):
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    is_default: Union[Unset, bool] = UNSET
    is_original_quality: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        id = self.id
        is_default = self.is_default
        is_original_quality = self.is_original_quality

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if description is not UNSET:
            field_dict["Description"] = description
        if id is not UNSET:
            field_dict["Id"] = id
        if is_default is not UNSET:
            field_dict["IsDefault"] = is_default
        if is_original_quality is not UNSET:
            field_dict["IsOriginalQuality"] = is_original_quality

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        description = d.pop("Description", UNSET)

        id = d.pop("Id", UNSET)

        is_default = d.pop("IsDefault", UNSET)

        is_original_quality = d.pop("IsOriginalQuality", UNSET)

        sync_model_sync_quality_option = cls(
            name=name,
            description=description,
            id=id,
            is_default=is_default,
            is_original_quality=is_original_quality,
        )

        sync_model_sync_quality_option.additional_properties = d
        return sync_model_sync_quality_option

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
