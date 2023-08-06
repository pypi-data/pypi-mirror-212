from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.emby_features_feature_type import EmbyFeaturesFeatureType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmbyFeaturesFeatureInfo")


@attr.s(auto_attribs=True)
class EmbyFeaturesFeatureInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        id (Union[Unset, str]):
        feature_type (Union[Unset, EmbyFeaturesFeatureType]):
    """

    name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    feature_type: Union[Unset, EmbyFeaturesFeatureType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        feature_type: Union[Unset, str] = UNSET
        if not isinstance(self.feature_type, Unset):
            feature_type = self.feature_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if id is not UNSET:
            field_dict["Id"] = id
        if feature_type is not UNSET:
            field_dict["FeatureType"] = feature_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        id = d.pop("Id", UNSET)

        _feature_type = d.pop("FeatureType", UNSET)
        feature_type: Union[Unset, EmbyFeaturesFeatureType]
        if isinstance(_feature_type, Unset):
            feature_type = UNSET
        else:
            feature_type = EmbyFeaturesFeatureType(_feature_type)

        emby_features_feature_info = cls(
            name=name,
            id=id,
            feature_type=feature_type,
        )

        emby_features_feature_info.additional_properties = d
        return emby_features_feature_info

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
