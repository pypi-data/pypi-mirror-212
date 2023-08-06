from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.providers_movie_info import ProvidersMovieInfo


T = TypeVar("T", bound="ProvidersRemoteSearchQueryProvidersMovieInfo")


@attr.s(auto_attribs=True)
class ProvidersRemoteSearchQueryProvidersMovieInfo:
    """
    Attributes:
        search_info (Union[Unset, ProvidersMovieInfo]):
        item_id (Union[Unset, int]):
        search_provider_name (Union[Unset, str]):
        providers (Union[Unset, List[str]]):
        include_disabled_providers (Union[Unset, bool]):
    """

    search_info: Union[Unset, "ProvidersMovieInfo"] = UNSET
    item_id: Union[Unset, int] = UNSET
    search_provider_name: Union[Unset, str] = UNSET
    providers: Union[Unset, List[str]] = UNSET
    include_disabled_providers: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        search_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.search_info, Unset):
            search_info = self.search_info.to_dict()

        item_id = self.item_id
        search_provider_name = self.search_provider_name
        providers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.providers, Unset):
            providers = self.providers

        include_disabled_providers = self.include_disabled_providers

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if search_info is not UNSET:
            field_dict["SearchInfo"] = search_info
        if item_id is not UNSET:
            field_dict["ItemId"] = item_id
        if search_provider_name is not UNSET:
            field_dict["SearchProviderName"] = search_provider_name
        if providers is not UNSET:
            field_dict["Providers"] = providers
        if include_disabled_providers is not UNSET:
            field_dict["IncludeDisabledProviders"] = include_disabled_providers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.providers_movie_info import ProvidersMovieInfo

        d = src_dict.copy()
        _search_info = d.pop("SearchInfo", UNSET)
        search_info: Union[Unset, ProvidersMovieInfo]
        if isinstance(_search_info, Unset):
            search_info = UNSET
        else:
            search_info = ProvidersMovieInfo.from_dict(_search_info)

        item_id = d.pop("ItemId", UNSET)

        search_provider_name = d.pop("SearchProviderName", UNSET)

        providers = cast(List[str], d.pop("Providers", UNSET))

        include_disabled_providers = d.pop("IncludeDisabledProviders", UNSET)

        providers_remote_search_query_providers_movie_info = cls(
            search_info=search_info,
            item_id=item_id,
            search_provider_name=search_provider_name,
            providers=providers,
            include_disabled_providers=include_disabled_providers,
        )

        providers_remote_search_query_providers_movie_info.additional_properties = d
        return providers_remote_search_query_providers_movie_info

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
