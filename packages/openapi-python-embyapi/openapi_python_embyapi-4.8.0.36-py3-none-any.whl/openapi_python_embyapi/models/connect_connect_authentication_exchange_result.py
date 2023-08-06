from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConnectConnectAuthenticationExchangeResult")


@attr.s(auto_attribs=True)
class ConnectConnectAuthenticationExchangeResult:
    """
    Attributes:
        local_user_id (Union[Unset, str]):
        access_token (Union[Unset, str]):
    """

    local_user_id: Union[Unset, str] = UNSET
    access_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        local_user_id = self.local_user_id
        access_token = self.access_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if local_user_id is not UNSET:
            field_dict["LocalUserId"] = local_user_id
        if access_token is not UNSET:
            field_dict["AccessToken"] = access_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        local_user_id = d.pop("LocalUserId", UNSET)

        access_token = d.pop("AccessToken", UNSET)

        connect_connect_authentication_exchange_result = cls(
            local_user_id=local_user_id,
            access_token=access_token,
        )

        connect_connect_authentication_exchange_result.additional_properties = d
        return connect_connect_authentication_exchange_result

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
