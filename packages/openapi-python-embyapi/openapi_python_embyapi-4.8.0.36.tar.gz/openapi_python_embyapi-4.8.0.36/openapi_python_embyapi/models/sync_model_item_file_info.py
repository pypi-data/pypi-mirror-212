from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.image_type import ImageType
from ..models.sync_model_item_file_type import SyncModelItemFileType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SyncModelItemFileInfo")


@attr.s(auto_attribs=True)
class SyncModelItemFileInfo:
    """
    Attributes:
        type (Union[Unset, SyncModelItemFileType]):
        name (Union[Unset, str]):
        path (Union[Unset, str]):
        image_type (Union[Unset, ImageType]):
        index (Union[Unset, int]):
    """

    type: Union[Unset, SyncModelItemFileType] = UNSET
    name: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    image_type: Union[Unset, ImageType] = UNSET
    index: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        name = self.name
        path = self.path
        image_type: Union[Unset, str] = UNSET
        if not isinstance(self.image_type, Unset):
            image_type = self.image_type.value

        index = self.index

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["Type"] = type
        if name is not UNSET:
            field_dict["Name"] = name
        if path is not UNSET:
            field_dict["Path"] = path
        if image_type is not UNSET:
            field_dict["ImageType"] = image_type
        if index is not UNSET:
            field_dict["Index"] = index

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("Type", UNSET)
        type: Union[Unset, SyncModelItemFileType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = SyncModelItemFileType(_type)

        name = d.pop("Name", UNSET)

        path = d.pop("Path", UNSET)

        _image_type = d.pop("ImageType", UNSET)
        image_type: Union[Unset, ImageType]
        if isinstance(_image_type, Unset):
            image_type = UNSET
        else:
            image_type = ImageType(_image_type)

        index = d.pop("Index", UNSET)

        sync_model_item_file_info = cls(
            type=type,
            name=name,
            path=path,
            image_type=image_type,
            index=index,
        )

        sync_model_item_file_info.additional_properties = d
        return sync_model_item_file_info

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
