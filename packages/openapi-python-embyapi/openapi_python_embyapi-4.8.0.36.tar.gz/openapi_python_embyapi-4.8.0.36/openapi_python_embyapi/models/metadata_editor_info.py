from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.external_id_info import ExternalIdInfo
    from ..models.globalization_country_info import GlobalizationCountryInfo
    from ..models.globalization_culture_dto import GlobalizationCultureDto
    from ..models.parental_rating import ParentalRating


T = TypeVar("T", bound="MetadataEditorInfo")


@attr.s(auto_attribs=True)
class MetadataEditorInfo:
    """
    Attributes:
        parental_rating_options (Union[Unset, List['ParentalRating']]):
        countries (Union[Unset, List['GlobalizationCountryInfo']]):
        cultures (Union[Unset, List['GlobalizationCultureDto']]):
        external_id_infos (Union[Unset, List['ExternalIdInfo']]):
    """

    parental_rating_options: Union[Unset, List["ParentalRating"]] = UNSET
    countries: Union[Unset, List["GlobalizationCountryInfo"]] = UNSET
    cultures: Union[Unset, List["GlobalizationCultureDto"]] = UNSET
    external_id_infos: Union[Unset, List["ExternalIdInfo"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        parental_rating_options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.parental_rating_options, Unset):
            parental_rating_options = []
            for parental_rating_options_item_data in self.parental_rating_options:
                parental_rating_options_item = parental_rating_options_item_data.to_dict()

                parental_rating_options.append(parental_rating_options_item)

        countries: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.countries, Unset):
            countries = []
            for countries_item_data in self.countries:
                countries_item = countries_item_data.to_dict()

                countries.append(countries_item)

        cultures: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.cultures, Unset):
            cultures = []
            for cultures_item_data in self.cultures:
                cultures_item = cultures_item_data.to_dict()

                cultures.append(cultures_item)

        external_id_infos: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.external_id_infos, Unset):
            external_id_infos = []
            for external_id_infos_item_data in self.external_id_infos:
                external_id_infos_item = external_id_infos_item_data.to_dict()

                external_id_infos.append(external_id_infos_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if parental_rating_options is not UNSET:
            field_dict["ParentalRatingOptions"] = parental_rating_options
        if countries is not UNSET:
            field_dict["Countries"] = countries
        if cultures is not UNSET:
            field_dict["Cultures"] = cultures
        if external_id_infos is not UNSET:
            field_dict["ExternalIdInfos"] = external_id_infos

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.external_id_info import ExternalIdInfo
        from ..models.globalization_country_info import GlobalizationCountryInfo
        from ..models.globalization_culture_dto import GlobalizationCultureDto
        from ..models.parental_rating import ParentalRating

        d = src_dict.copy()
        parental_rating_options = []
        _parental_rating_options = d.pop("ParentalRatingOptions", UNSET)
        for parental_rating_options_item_data in _parental_rating_options or []:
            parental_rating_options_item = ParentalRating.from_dict(parental_rating_options_item_data)

            parental_rating_options.append(parental_rating_options_item)

        countries = []
        _countries = d.pop("Countries", UNSET)
        for countries_item_data in _countries or []:
            countries_item = GlobalizationCountryInfo.from_dict(countries_item_data)

            countries.append(countries_item)

        cultures = []
        _cultures = d.pop("Cultures", UNSET)
        for cultures_item_data in _cultures or []:
            cultures_item = GlobalizationCultureDto.from_dict(cultures_item_data)

            cultures.append(cultures_item)

        external_id_infos = []
        _external_id_infos = d.pop("ExternalIdInfos", UNSET)
        for external_id_infos_item_data in _external_id_infos or []:
            external_id_infos_item = ExternalIdInfo.from_dict(external_id_infos_item_data)

            external_id_infos.append(external_id_infos_item)

        metadata_editor_info = cls(
            parental_rating_options=parental_rating_options,
            countries=countries,
            cultures=cultures,
            external_id_infos=external_id_infos,
        )

        metadata_editor_info.additional_properties = d
        return metadata_editor_info

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
