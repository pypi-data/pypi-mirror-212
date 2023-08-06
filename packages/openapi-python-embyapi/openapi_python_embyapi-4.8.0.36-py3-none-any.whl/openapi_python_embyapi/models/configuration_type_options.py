from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.configuration_image_option import ConfigurationImageOption


T = TypeVar("T", bound="ConfigurationTypeOptions")


@attr.s(auto_attribs=True)
class ConfigurationTypeOptions:
    """
    Attributes:
        type (Union[Unset, str]):
        metadata_fetchers (Union[Unset, List[str]]):
        metadata_fetcher_order (Union[Unset, List[str]]):
        image_fetchers (Union[Unset, List[str]]):
        image_fetcher_order (Union[Unset, List[str]]):
        image_options (Union[Unset, List['ConfigurationImageOption']]):
    """

    type: Union[Unset, str] = UNSET
    metadata_fetchers: Union[Unset, List[str]] = UNSET
    metadata_fetcher_order: Union[Unset, List[str]] = UNSET
    image_fetchers: Union[Unset, List[str]] = UNSET
    image_fetcher_order: Union[Unset, List[str]] = UNSET
    image_options: Union[Unset, List["ConfigurationImageOption"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        metadata_fetchers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.metadata_fetchers, Unset):
            metadata_fetchers = self.metadata_fetchers

        metadata_fetcher_order: Union[Unset, List[str]] = UNSET
        if not isinstance(self.metadata_fetcher_order, Unset):
            metadata_fetcher_order = self.metadata_fetcher_order

        image_fetchers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.image_fetchers, Unset):
            image_fetchers = self.image_fetchers

        image_fetcher_order: Union[Unset, List[str]] = UNSET
        if not isinstance(self.image_fetcher_order, Unset):
            image_fetcher_order = self.image_fetcher_order

        image_options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.image_options, Unset):
            image_options = []
            for image_options_item_data in self.image_options:
                image_options_item = image_options_item_data.to_dict()

                image_options.append(image_options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["Type"] = type
        if metadata_fetchers is not UNSET:
            field_dict["MetadataFetchers"] = metadata_fetchers
        if metadata_fetcher_order is not UNSET:
            field_dict["MetadataFetcherOrder"] = metadata_fetcher_order
        if image_fetchers is not UNSET:
            field_dict["ImageFetchers"] = image_fetchers
        if image_fetcher_order is not UNSET:
            field_dict["ImageFetcherOrder"] = image_fetcher_order
        if image_options is not UNSET:
            field_dict["ImageOptions"] = image_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.configuration_image_option import ConfigurationImageOption

        d = src_dict.copy()
        type = d.pop("Type", UNSET)

        metadata_fetchers = cast(List[str], d.pop("MetadataFetchers", UNSET))

        metadata_fetcher_order = cast(List[str], d.pop("MetadataFetcherOrder", UNSET))

        image_fetchers = cast(List[str], d.pop("ImageFetchers", UNSET))

        image_fetcher_order = cast(List[str], d.pop("ImageFetcherOrder", UNSET))

        image_options = []
        _image_options = d.pop("ImageOptions", UNSET)
        for image_options_item_data in _image_options or []:
            image_options_item = ConfigurationImageOption.from_dict(image_options_item_data)

            image_options.append(image_options_item)

        configuration_type_options = cls(
            type=type,
            metadata_fetchers=metadata_fetchers,
            metadata_fetcher_order=metadata_fetcher_order,
            image_fetchers=image_fetchers,
            image_fetcher_order=image_fetcher_order,
            image_options=image_options,
        )

        configuration_type_options.additional_properties = d
        return configuration_type_options

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
