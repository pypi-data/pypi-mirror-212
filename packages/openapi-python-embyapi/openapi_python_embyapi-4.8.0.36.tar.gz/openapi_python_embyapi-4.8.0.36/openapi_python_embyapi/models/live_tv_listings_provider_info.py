from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.name_value_pair import NameValuePair


T = TypeVar("T", bound="LiveTvListingsProviderInfo")


@attr.s(auto_attribs=True)
class LiveTvListingsProviderInfo:
    """
    Attributes:
        name (Union[Unset, str]):
        setup_url (Union[Unset, str]):
        id (Union[Unset, str]):
        type (Union[Unset, str]):
        username (Union[Unset, str]):
        password (Union[Unset, str]):
        listings_id (Union[Unset, str]):
        zip_code (Union[Unset, str]):
        country (Union[Unset, str]):
        path (Union[Unset, str]):
        enabled_tuners (Union[Unset, List[str]]):
        enable_all_tuners (Union[Unset, bool]):
        news_categories (Union[Unset, List[str]]):
        sports_categories (Union[Unset, List[str]]):
        kids_categories (Union[Unset, List[str]]):
        movie_categories (Union[Unset, List[str]]):
        channel_mappings (Union[Unset, List['NameValuePair']]):
        movie_prefix (Union[Unset, str]):
        preferred_language (Union[Unset, str]):
        user_agent (Union[Unset, str]):
        data_version (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    setup_url: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    listings_id: Union[Unset, str] = UNSET
    zip_code: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    enabled_tuners: Union[Unset, List[str]] = UNSET
    enable_all_tuners: Union[Unset, bool] = UNSET
    news_categories: Union[Unset, List[str]] = UNSET
    sports_categories: Union[Unset, List[str]] = UNSET
    kids_categories: Union[Unset, List[str]] = UNSET
    movie_categories: Union[Unset, List[str]] = UNSET
    channel_mappings: Union[Unset, List["NameValuePair"]] = UNSET
    movie_prefix: Union[Unset, str] = UNSET
    preferred_language: Union[Unset, str] = UNSET
    user_agent: Union[Unset, str] = UNSET
    data_version: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        setup_url = self.setup_url
        id = self.id
        type = self.type
        username = self.username
        password = self.password
        listings_id = self.listings_id
        zip_code = self.zip_code
        country = self.country
        path = self.path
        enabled_tuners: Union[Unset, List[str]] = UNSET
        if not isinstance(self.enabled_tuners, Unset):
            enabled_tuners = self.enabled_tuners

        enable_all_tuners = self.enable_all_tuners
        news_categories: Union[Unset, List[str]] = UNSET
        if not isinstance(self.news_categories, Unset):
            news_categories = self.news_categories

        sports_categories: Union[Unset, List[str]] = UNSET
        if not isinstance(self.sports_categories, Unset):
            sports_categories = self.sports_categories

        kids_categories: Union[Unset, List[str]] = UNSET
        if not isinstance(self.kids_categories, Unset):
            kids_categories = self.kids_categories

        movie_categories: Union[Unset, List[str]] = UNSET
        if not isinstance(self.movie_categories, Unset):
            movie_categories = self.movie_categories

        channel_mappings: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.channel_mappings, Unset):
            channel_mappings = []
            for channel_mappings_item_data in self.channel_mappings:
                channel_mappings_item = channel_mappings_item_data.to_dict()

                channel_mappings.append(channel_mappings_item)

        movie_prefix = self.movie_prefix
        preferred_language = self.preferred_language
        user_agent = self.user_agent
        data_version = self.data_version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if setup_url is not UNSET:
            field_dict["SetupUrl"] = setup_url
        if id is not UNSET:
            field_dict["Id"] = id
        if type is not UNSET:
            field_dict["Type"] = type
        if username is not UNSET:
            field_dict["Username"] = username
        if password is not UNSET:
            field_dict["Password"] = password
        if listings_id is not UNSET:
            field_dict["ListingsId"] = listings_id
        if zip_code is not UNSET:
            field_dict["ZipCode"] = zip_code
        if country is not UNSET:
            field_dict["Country"] = country
        if path is not UNSET:
            field_dict["Path"] = path
        if enabled_tuners is not UNSET:
            field_dict["EnabledTuners"] = enabled_tuners
        if enable_all_tuners is not UNSET:
            field_dict["EnableAllTuners"] = enable_all_tuners
        if news_categories is not UNSET:
            field_dict["NewsCategories"] = news_categories
        if sports_categories is not UNSET:
            field_dict["SportsCategories"] = sports_categories
        if kids_categories is not UNSET:
            field_dict["KidsCategories"] = kids_categories
        if movie_categories is not UNSET:
            field_dict["MovieCategories"] = movie_categories
        if channel_mappings is not UNSET:
            field_dict["ChannelMappings"] = channel_mappings
        if movie_prefix is not UNSET:
            field_dict["MoviePrefix"] = movie_prefix
        if preferred_language is not UNSET:
            field_dict["PreferredLanguage"] = preferred_language
        if user_agent is not UNSET:
            field_dict["UserAgent"] = user_agent
        if data_version is not UNSET:
            field_dict["DataVersion"] = data_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.name_value_pair import NameValuePair

        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        setup_url = d.pop("SetupUrl", UNSET)

        id = d.pop("Id", UNSET)

        type = d.pop("Type", UNSET)

        username = d.pop("Username", UNSET)

        password = d.pop("Password", UNSET)

        listings_id = d.pop("ListingsId", UNSET)

        zip_code = d.pop("ZipCode", UNSET)

        country = d.pop("Country", UNSET)

        path = d.pop("Path", UNSET)

        enabled_tuners = cast(List[str], d.pop("EnabledTuners", UNSET))

        enable_all_tuners = d.pop("EnableAllTuners", UNSET)

        news_categories = cast(List[str], d.pop("NewsCategories", UNSET))

        sports_categories = cast(List[str], d.pop("SportsCategories", UNSET))

        kids_categories = cast(List[str], d.pop("KidsCategories", UNSET))

        movie_categories = cast(List[str], d.pop("MovieCategories", UNSET))

        channel_mappings = []
        _channel_mappings = d.pop("ChannelMappings", UNSET)
        for channel_mappings_item_data in _channel_mappings or []:
            channel_mappings_item = NameValuePair.from_dict(channel_mappings_item_data)

            channel_mappings.append(channel_mappings_item)

        movie_prefix = d.pop("MoviePrefix", UNSET)

        preferred_language = d.pop("PreferredLanguage", UNSET)

        user_agent = d.pop("UserAgent", UNSET)

        data_version = d.pop("DataVersion", UNSET)

        live_tv_listings_provider_info = cls(
            name=name,
            setup_url=setup_url,
            id=id,
            type=type,
            username=username,
            password=password,
            listings_id=listings_id,
            zip_code=zip_code,
            country=country,
            path=path,
            enabled_tuners=enabled_tuners,
            enable_all_tuners=enable_all_tuners,
            news_categories=news_categories,
            sports_categories=sports_categories,
            kids_categories=kids_categories,
            movie_categories=movie_categories,
            channel_mappings=channel_mappings,
            movie_prefix=movie_prefix,
            preferred_language=preferred_language,
            user_agent=user_agent,
            data_version=data_version,
        )

        live_tv_listings_provider_info.additional_properties = d
        return live_tv_listings_provider_info

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
