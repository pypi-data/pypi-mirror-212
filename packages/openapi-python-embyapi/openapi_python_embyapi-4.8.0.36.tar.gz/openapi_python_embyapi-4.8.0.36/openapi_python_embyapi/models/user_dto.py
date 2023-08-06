import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.connect_user_link_type import ConnectUserLinkType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.configuration_user_configuration import ConfigurationUserConfiguration
    from ..models.users_user_policy import UsersUserPolicy


T = TypeVar("T", bound="UserDto")


@attr.s(auto_attribs=True)
class UserDto:
    """
    Attributes:
        name (Union[Unset, str]):
        server_id (Union[Unset, str]):
        server_name (Union[Unset, str]):
        prefix (Union[Unset, str]):
        connect_user_name (Union[Unset, str]):
        date_created (Union[Unset, None, datetime.datetime]):
        connect_link_type (Union[Unset, ConnectUserLinkType]):
        id (Union[Unset, str]):
        primary_image_tag (Union[Unset, str]):
        has_password (Union[Unset, bool]):
        has_configured_password (Union[Unset, bool]):
        has_configured_easy_password (Union[Unset, bool]):
        enable_auto_login (Union[Unset, None, bool]):
        last_login_date (Union[Unset, None, datetime.datetime]):
        last_activity_date (Union[Unset, None, datetime.datetime]):
        configuration (Union[Unset, ConfigurationUserConfiguration]):
        policy (Union[Unset, UsersUserPolicy]):
        primary_image_aspect_ratio (Union[Unset, None, float]):
    """

    name: Union[Unset, str] = UNSET
    server_id: Union[Unset, str] = UNSET
    server_name: Union[Unset, str] = UNSET
    prefix: Union[Unset, str] = UNSET
    connect_user_name: Union[Unset, str] = UNSET
    date_created: Union[Unset, None, datetime.datetime] = UNSET
    connect_link_type: Union[Unset, ConnectUserLinkType] = UNSET
    id: Union[Unset, str] = UNSET
    primary_image_tag: Union[Unset, str] = UNSET
    has_password: Union[Unset, bool] = UNSET
    has_configured_password: Union[Unset, bool] = UNSET
    has_configured_easy_password: Union[Unset, bool] = UNSET
    enable_auto_login: Union[Unset, None, bool] = UNSET
    last_login_date: Union[Unset, None, datetime.datetime] = UNSET
    last_activity_date: Union[Unset, None, datetime.datetime] = UNSET
    configuration: Union[Unset, "ConfigurationUserConfiguration"] = UNSET
    policy: Union[Unset, "UsersUserPolicy"] = UNSET
    primary_image_aspect_ratio: Union[Unset, None, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        server_id = self.server_id
        server_name = self.server_name
        prefix = self.prefix
        connect_user_name = self.connect_user_name
        date_created: Union[Unset, None, str] = UNSET
        if not isinstance(self.date_created, Unset):
            date_created = self.date_created.isoformat() if self.date_created else None

        connect_link_type: Union[Unset, str] = UNSET
        if not isinstance(self.connect_link_type, Unset):
            connect_link_type = self.connect_link_type.value

        id = self.id
        primary_image_tag = self.primary_image_tag
        has_password = self.has_password
        has_configured_password = self.has_configured_password
        has_configured_easy_password = self.has_configured_easy_password
        enable_auto_login = self.enable_auto_login
        last_login_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_login_date, Unset):
            last_login_date = self.last_login_date.isoformat() if self.last_login_date else None

        last_activity_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_activity_date, Unset):
            last_activity_date = self.last_activity_date.isoformat() if self.last_activity_date else None

        configuration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.configuration, Unset):
            configuration = self.configuration.to_dict()

        policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.policy, Unset):
            policy = self.policy.to_dict()

        primary_image_aspect_ratio = self.primary_image_aspect_ratio

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if server_id is not UNSET:
            field_dict["ServerId"] = server_id
        if server_name is not UNSET:
            field_dict["ServerName"] = server_name
        if prefix is not UNSET:
            field_dict["Prefix"] = prefix
        if connect_user_name is not UNSET:
            field_dict["ConnectUserName"] = connect_user_name
        if date_created is not UNSET:
            field_dict["DateCreated"] = date_created
        if connect_link_type is not UNSET:
            field_dict["ConnectLinkType"] = connect_link_type
        if id is not UNSET:
            field_dict["Id"] = id
        if primary_image_tag is not UNSET:
            field_dict["PrimaryImageTag"] = primary_image_tag
        if has_password is not UNSET:
            field_dict["HasPassword"] = has_password
        if has_configured_password is not UNSET:
            field_dict["HasConfiguredPassword"] = has_configured_password
        if has_configured_easy_password is not UNSET:
            field_dict["HasConfiguredEasyPassword"] = has_configured_easy_password
        if enable_auto_login is not UNSET:
            field_dict["EnableAutoLogin"] = enable_auto_login
        if last_login_date is not UNSET:
            field_dict["LastLoginDate"] = last_login_date
        if last_activity_date is not UNSET:
            field_dict["LastActivityDate"] = last_activity_date
        if configuration is not UNSET:
            field_dict["Configuration"] = configuration
        if policy is not UNSET:
            field_dict["Policy"] = policy
        if primary_image_aspect_ratio is not UNSET:
            field_dict["PrimaryImageAspectRatio"] = primary_image_aspect_ratio

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.configuration_user_configuration import ConfigurationUserConfiguration
        from ..models.users_user_policy import UsersUserPolicy

        d = src_dict.copy()
        name = d.pop("Name", UNSET)

        server_id = d.pop("ServerId", UNSET)

        server_name = d.pop("ServerName", UNSET)

        prefix = d.pop("Prefix", UNSET)

        connect_user_name = d.pop("ConnectUserName", UNSET)

        _date_created = d.pop("DateCreated", UNSET)
        date_created: Union[Unset, None, datetime.datetime]
        if _date_created is None:
            date_created = None
        elif isinstance(_date_created, Unset):
            date_created = UNSET
        else:
            date_created = isoparse(_date_created)

        _connect_link_type = d.pop("ConnectLinkType", UNSET)
        connect_link_type: Union[Unset, ConnectUserLinkType]
        if isinstance(_connect_link_type, Unset):
            connect_link_type = UNSET
        else:
            connect_link_type = ConnectUserLinkType(_connect_link_type)

        id = d.pop("Id", UNSET)

        primary_image_tag = d.pop("PrimaryImageTag", UNSET)

        has_password = d.pop("HasPassword", UNSET)

        has_configured_password = d.pop("HasConfiguredPassword", UNSET)

        has_configured_easy_password = d.pop("HasConfiguredEasyPassword", UNSET)

        enable_auto_login = d.pop("EnableAutoLogin", UNSET)

        _last_login_date = d.pop("LastLoginDate", UNSET)
        last_login_date: Union[Unset, None, datetime.datetime]
        if _last_login_date is None:
            last_login_date = None
        elif isinstance(_last_login_date, Unset):
            last_login_date = UNSET
        else:
            last_login_date = isoparse(_last_login_date)

        _last_activity_date = d.pop("LastActivityDate", UNSET)
        last_activity_date: Union[Unset, None, datetime.datetime]
        if _last_activity_date is None:
            last_activity_date = None
        elif isinstance(_last_activity_date, Unset):
            last_activity_date = UNSET
        else:
            last_activity_date = isoparse(_last_activity_date)

        _configuration = d.pop("Configuration", UNSET)
        configuration: Union[Unset, ConfigurationUserConfiguration]
        if isinstance(_configuration, Unset):
            configuration = UNSET
        else:
            configuration = ConfigurationUserConfiguration.from_dict(_configuration)

        _policy = d.pop("Policy", UNSET)
        policy: Union[Unset, UsersUserPolicy]
        if isinstance(_policy, Unset):
            policy = UNSET
        else:
            policy = UsersUserPolicy.from_dict(_policy)

        primary_image_aspect_ratio = d.pop("PrimaryImageAspectRatio", UNSET)

        user_dto = cls(
            name=name,
            server_id=server_id,
            server_name=server_name,
            prefix=prefix,
            connect_user_name=connect_user_name,
            date_created=date_created,
            connect_link_type=connect_link_type,
            id=id,
            primary_image_tag=primary_image_tag,
            has_password=has_password,
            has_configured_password=has_configured_password,
            has_configured_easy_password=has_configured_easy_password,
            enable_auto_login=enable_auto_login,
            last_login_date=last_login_date,
            last_activity_date=last_activity_date,
            configuration=configuration,
            policy=policy,
            primary_image_aspect_ratio=primary_image_aspect_ratio,
        )

        user_dto.additional_properties = d
        return user_dto

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
