from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.session_session_info import SessionSessionInfo
    from ..models.user_dto import UserDto


T = TypeVar("T", bound="AuthenticationAuthenticationResult")


@attr.s(auto_attribs=True)
class AuthenticationAuthenticationResult:
    """
    Attributes:
        user (Union[Unset, UserDto]):
        session_info (Union[Unset, SessionSessionInfo]):
        access_token (Union[Unset, str]):
        server_id (Union[Unset, str]):
    """

    user: Union[Unset, "UserDto"] = UNSET
    session_info: Union[Unset, "SessionSessionInfo"] = UNSET
    access_token: Union[Unset, str] = UNSET
    server_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        session_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.session_info, Unset):
            session_info = self.session_info.to_dict()

        access_token = self.access_token
        server_id = self.server_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user is not UNSET:
            field_dict["User"] = user
        if session_info is not UNSET:
            field_dict["SessionInfo"] = session_info
        if access_token is not UNSET:
            field_dict["AccessToken"] = access_token
        if server_id is not UNSET:
            field_dict["ServerId"] = server_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.session_session_info import SessionSessionInfo
        from ..models.user_dto import UserDto

        d = src_dict.copy()
        _user = d.pop("User", UNSET)
        user: Union[Unset, UserDto]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = UserDto.from_dict(_user)

        _session_info = d.pop("SessionInfo", UNSET)
        session_info: Union[Unset, SessionSessionInfo]
        if isinstance(_session_info, Unset):
            session_info = UNSET
        else:
            session_info = SessionSessionInfo.from_dict(_session_info)

        access_token = d.pop("AccessToken", UNSET)

        server_id = d.pop("ServerId", UNSET)

        authentication_authentication_result = cls(
            user=user,
            session_info=session_info,
            access_token=access_token,
            server_id=server_id,
        )

        authentication_authentication_result.additional_properties = d
        return authentication_authentication_result

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
