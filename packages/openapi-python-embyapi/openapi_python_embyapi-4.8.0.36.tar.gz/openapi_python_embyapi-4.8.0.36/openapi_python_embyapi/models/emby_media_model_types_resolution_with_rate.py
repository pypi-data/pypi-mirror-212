from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.emby_media_model_types_resolution import EmbyMediaModelTypesResolution


T = TypeVar("T", bound="EmbyMediaModelTypesResolutionWithRate")


@attr.s(auto_attribs=True)
class EmbyMediaModelTypesResolutionWithRate:
    """
    Attributes:
        width (Union[Unset, int]):
        height (Union[Unset, int]):
        frame_rate (Union[Unset, float]):
        resolution (Union[Unset, EmbyMediaModelTypesResolution]):
    """

    width: Union[Unset, int] = UNSET
    height: Union[Unset, int] = UNSET
    frame_rate: Union[Unset, float] = UNSET
    resolution: Union[Unset, "EmbyMediaModelTypesResolution"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        width = self.width
        height = self.height
        frame_rate = self.frame_rate
        resolution: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resolution, Unset):
            resolution = self.resolution.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if width is not UNSET:
            field_dict["Width"] = width
        if height is not UNSET:
            field_dict["Height"] = height
        if frame_rate is not UNSET:
            field_dict["FrameRate"] = frame_rate
        if resolution is not UNSET:
            field_dict["Resolution"] = resolution

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.emby_media_model_types_resolution import EmbyMediaModelTypesResolution

        d = src_dict.copy()
        width = d.pop("Width", UNSET)

        height = d.pop("Height", UNSET)

        frame_rate = d.pop("FrameRate", UNSET)

        _resolution = d.pop("Resolution", UNSET)
        resolution: Union[Unset, EmbyMediaModelTypesResolution]
        if isinstance(_resolution, Unset):
            resolution = UNSET
        else:
            resolution = EmbyMediaModelTypesResolution.from_dict(_resolution)

        emby_media_model_types_resolution_with_rate = cls(
            width=width,
            height=height,
            frame_rate=frame_rate,
            resolution=resolution,
        )

        emby_media_model_types_resolution_with_rate.additional_properties = d
        return emby_media_model_types_resolution_with_rate

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
