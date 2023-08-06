from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.emby_media_model_types_bit_rate import EmbyMediaModelTypesBitRate
    from ..models.emby_media_model_types_resolution_with_rate import EmbyMediaModelTypesResolutionWithRate


T = TypeVar("T", bound="EmbyMediaModelTypesLevelInformation")


@attr.s(auto_attribs=True)
class EmbyMediaModelTypesLevelInformation:
    """
    Attributes:
        short_name (Union[Unset, str]):
        description (Union[Unset, str]):
        ordinal (Union[Unset, None, int]):
        max_bit_rate (Union[Unset, EmbyMediaModelTypesBitRate]):
        max_bit_rate_display (Union[Unset, str]):
        id (Union[Unset, str]):
        resolution_rates (Union[Unset, List['EmbyMediaModelTypesResolutionWithRate']]):
        resolution_rate_strings (Union[Unset, List[str]]):
        resolution_rates_display (Union[Unset, str]):
    """

    short_name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    ordinal: Union[Unset, None, int] = UNSET
    max_bit_rate: Union[Unset, "EmbyMediaModelTypesBitRate"] = UNSET
    max_bit_rate_display: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    resolution_rates: Union[Unset, List["EmbyMediaModelTypesResolutionWithRate"]] = UNSET
    resolution_rate_strings: Union[Unset, List[str]] = UNSET
    resolution_rates_display: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        short_name = self.short_name
        description = self.description
        ordinal = self.ordinal
        max_bit_rate: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.max_bit_rate, Unset):
            max_bit_rate = self.max_bit_rate.to_dict()

        max_bit_rate_display = self.max_bit_rate_display
        id = self.id
        resolution_rates: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.resolution_rates, Unset):
            resolution_rates = []
            for resolution_rates_item_data in self.resolution_rates:
                resolution_rates_item = resolution_rates_item_data.to_dict()

                resolution_rates.append(resolution_rates_item)

        resolution_rate_strings: Union[Unset, List[str]] = UNSET
        if not isinstance(self.resolution_rate_strings, Unset):
            resolution_rate_strings = self.resolution_rate_strings

        resolution_rates_display = self.resolution_rates_display

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if short_name is not UNSET:
            field_dict["ShortName"] = short_name
        if description is not UNSET:
            field_dict["Description"] = description
        if ordinal is not UNSET:
            field_dict["Ordinal"] = ordinal
        if max_bit_rate is not UNSET:
            field_dict["MaxBitRate"] = max_bit_rate
        if max_bit_rate_display is not UNSET:
            field_dict["MaxBitRateDisplay"] = max_bit_rate_display
        if id is not UNSET:
            field_dict["Id"] = id
        if resolution_rates is not UNSET:
            field_dict["ResolutionRates"] = resolution_rates
        if resolution_rate_strings is not UNSET:
            field_dict["ResolutionRateStrings"] = resolution_rate_strings
        if resolution_rates_display is not UNSET:
            field_dict["ResolutionRatesDisplay"] = resolution_rates_display

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.emby_media_model_types_bit_rate import EmbyMediaModelTypesBitRate
        from ..models.emby_media_model_types_resolution_with_rate import EmbyMediaModelTypesResolutionWithRate

        d = src_dict.copy()
        short_name = d.pop("ShortName", UNSET)

        description = d.pop("Description", UNSET)

        ordinal = d.pop("Ordinal", UNSET)

        _max_bit_rate = d.pop("MaxBitRate", UNSET)
        max_bit_rate: Union[Unset, EmbyMediaModelTypesBitRate]
        if isinstance(_max_bit_rate, Unset):
            max_bit_rate = UNSET
        else:
            max_bit_rate = EmbyMediaModelTypesBitRate.from_dict(_max_bit_rate)

        max_bit_rate_display = d.pop("MaxBitRateDisplay", UNSET)

        id = d.pop("Id", UNSET)

        resolution_rates = []
        _resolution_rates = d.pop("ResolutionRates", UNSET)
        for resolution_rates_item_data in _resolution_rates or []:
            resolution_rates_item = EmbyMediaModelTypesResolutionWithRate.from_dict(resolution_rates_item_data)

            resolution_rates.append(resolution_rates_item)

        resolution_rate_strings = cast(List[str], d.pop("ResolutionRateStrings", UNSET))

        resolution_rates_display = d.pop("ResolutionRatesDisplay", UNSET)

        emby_media_model_types_level_information = cls(
            short_name=short_name,
            description=description,
            ordinal=ordinal,
            max_bit_rate=max_bit_rate,
            max_bit_rate_display=max_bit_rate_display,
            id=id,
            resolution_rates=resolution_rates,
            resolution_rate_strings=resolution_rate_strings,
            resolution_rates_display=resolution_rates_display,
        )

        emby_media_model_types_level_information.additional_properties = d
        return emby_media_model_types_level_information

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
