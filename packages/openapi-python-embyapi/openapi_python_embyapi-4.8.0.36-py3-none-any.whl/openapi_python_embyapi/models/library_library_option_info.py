from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.configuration_metadata_features import ConfigurationMetadataFeatures
from ..types import UNSET, Unset

T = TypeVar("T", bound="LibraryLibraryOptionInfo")


@attr.s(auto_attribs=True)
class LibraryLibraryOptionInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        setup_url (Union[Unset, str]):
        default_enabled (Union[Unset, bool]):
        features (Union[Unset, List[ConfigurationMetadataFeatures]]):
    """

    name: Union[Unset, str] = UNSET
    setup_url: Union[Unset, str] = UNSET
    default_enabled: Union[Unset, bool] = UNSET
    features: Union[Unset, List[ConfigurationMetadataFeatures]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        setup_url = self.setup_url
        default_enabled = self.default_enabled
        features: Union[Unset, List[str]] = UNSET
        if not isinstance(self.features, Unset):
            features = []
            for features_item_data in self.features:
                features_item = features_item_data.value

                features.append(features_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if setup_url is not UNSET:
            field_dict["SetupUrl"] = setup_url
        if default_enabled is not UNSET:
            field_dict["DefaultEnabled"] = default_enabled
        if features is not UNSET:
            field_dict["Features"] = features

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        setup_url = d.pop("SetupUrl", UNSET)

        default_enabled = d.pop("DefaultEnabled", UNSET)

        features = []
        _features = d.pop("Features", UNSET)
        for features_item_data in _features or []:
            features_item = ConfigurationMetadataFeatures(features_item_data)

            features.append(features_item)

        library_library_option_info = cls(
            name=name,
            setup_url=setup_url,
            default_enabled=default_enabled,
            features=features,
        )

        library_library_option_info.additional_properties = d
        return library_library_option_info

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
