import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.globalization_culture_dto import GlobalizationCultureDto
    from ..models.provider_id_dictionary import ProviderIdDictionary


T = TypeVar("T", bound="ProvidersBookInfo")


@attr.s(auto_attribs=True)
class ProvidersBookInfo:
    """
    Attributes:
        series_name (Union[Unset, str]):
        name (Union[Unset, str]):
        metadata_language (Union[Unset, str]):
        metadata_country_code (Union[Unset, str]):
        metadata_languages (Union[Unset, List['GlobalizationCultureDto']]):
        provider_ids (Union[Unset, ProviderIdDictionary]):
        year (Union[Unset, None, int]):
        index_number (Union[Unset, None, int]):
        parent_index_number (Union[Unset, None, int]):
        premiere_date (Union[Unset, None, datetime.datetime]):
        is_automated (Union[Unset, bool]):
        enable_adult_metadata (Union[Unset, bool]):
    """

    series_name: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    metadata_language: Union[Unset, str] = UNSET
    metadata_country_code: Union[Unset, str] = UNSET
    metadata_languages: Union[Unset, List["GlobalizationCultureDto"]] = UNSET
    provider_ids: Union[Unset, "ProviderIdDictionary"] = UNSET
    year: Union[Unset, None, int] = UNSET
    index_number: Union[Unset, None, int] = UNSET
    parent_index_number: Union[Unset, None, int] = UNSET
    premiere_date: Union[Unset, None, datetime.datetime] = UNSET
    is_automated: Union[Unset, bool] = UNSET
    enable_adult_metadata: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        series_name = self.series_name
        name = self.name
        metadata_language = self.metadata_language
        metadata_country_code = self.metadata_country_code
        metadata_languages: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.metadata_languages, Unset):
            metadata_languages = []
            for metadata_languages_item_data in self.metadata_languages:
                metadata_languages_item = metadata_languages_item_data.to_dict()

                metadata_languages.append(metadata_languages_item)

        provider_ids: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.provider_ids, Unset):
            provider_ids = self.provider_ids.to_dict()

        year = self.year
        index_number = self.index_number
        parent_index_number = self.parent_index_number
        premiere_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.premiere_date, Unset):
            premiere_date = self.premiere_date.isoformat() if self.premiere_date else None

        is_automated = self.is_automated
        enable_adult_metadata = self.enable_adult_metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if series_name is not UNSET:
            field_dict["SeriesName"] = series_name
        if name is not UNSET:
            field_dict["Name"] = name
        if metadata_language is not UNSET:
            field_dict["MetadataLanguage"] = metadata_language
        if metadata_country_code is not UNSET:
            field_dict["MetadataCountryCode"] = metadata_country_code
        if metadata_languages is not UNSET:
            field_dict["MetadataLanguages"] = metadata_languages
        if provider_ids is not UNSET:
            field_dict["ProviderIds"] = provider_ids
        if year is not UNSET:
            field_dict["Year"] = year
        if index_number is not UNSET:
            field_dict["IndexNumber"] = index_number
        if parent_index_number is not UNSET:
            field_dict["ParentIndexNumber"] = parent_index_number
        if premiere_date is not UNSET:
            field_dict["PremiereDate"] = premiere_date
        if is_automated is not UNSET:
            field_dict["IsAutomated"] = is_automated
        if enable_adult_metadata is not UNSET:
            field_dict["EnableAdultMetadata"] = enable_adult_metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.globalization_culture_dto import GlobalizationCultureDto
        from ..models.provider_id_dictionary import ProviderIdDictionary

        d = src_dict.copy()
        series_name = d.pop("SeriesName", UNSET)

        name = d.pop("Name", UNSET)

        metadata_language = d.pop("MetadataLanguage", UNSET)

        metadata_country_code = d.pop("MetadataCountryCode", UNSET)

        metadata_languages = []
        _metadata_languages = d.pop("MetadataLanguages", UNSET)
        for metadata_languages_item_data in _metadata_languages or []:
            metadata_languages_item = GlobalizationCultureDto.from_dict(metadata_languages_item_data)

            metadata_languages.append(metadata_languages_item)

        _provider_ids = d.pop("ProviderIds", UNSET)
        provider_ids: Union[Unset, ProviderIdDictionary]
        if isinstance(_provider_ids, Unset):
            provider_ids = UNSET
        else:
            provider_ids = ProviderIdDictionary.from_dict(_provider_ids)

        year = d.pop("Year", UNSET)

        index_number = d.pop("IndexNumber", UNSET)

        parent_index_number = d.pop("ParentIndexNumber", UNSET)

        _premiere_date = d.pop("PremiereDate", UNSET)
        premiere_date: Union[Unset, None, datetime.datetime]
        if _premiere_date is None:
            premiere_date = None
        elif isinstance(_premiere_date, Unset):
            premiere_date = UNSET
        else:
            premiere_date = isoparse(_premiere_date)

        is_automated = d.pop("IsAutomated", UNSET)

        enable_adult_metadata = d.pop("EnableAdultMetadata", UNSET)

        providers_book_info = cls(
            series_name=series_name,
            name=name,
            metadata_language=metadata_language,
            metadata_country_code=metadata_country_code,
            metadata_languages=metadata_languages,
            provider_ids=provider_ids,
            year=year,
            index_number=index_number,
            parent_index_number=parent_index_number,
            premiere_date=premiere_date,
            is_automated=is_automated,
            enable_adult_metadata=enable_adult_metadata,
        )

        providers_book_info.additional_properties = d
        return providers_book_info

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
