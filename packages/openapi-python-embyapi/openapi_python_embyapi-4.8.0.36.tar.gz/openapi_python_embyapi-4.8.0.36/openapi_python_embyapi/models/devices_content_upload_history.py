from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.devices_local_file_info import DevicesLocalFileInfo


T = TypeVar("T", bound="DevicesContentUploadHistory")


@attr.s(auto_attribs=True)
class DevicesContentUploadHistory:
    """
    Attributes:
        device_id (Union[Unset, str]):
        files_uploaded (Union[Unset, List['DevicesLocalFileInfo']]):
    """

    device_id: Union[Unset, str] = UNSET
    files_uploaded: Union[Unset, List["DevicesLocalFileInfo"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        device_id = self.device_id
        files_uploaded: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.files_uploaded, Unset):
            files_uploaded = []
            for files_uploaded_item_data in self.files_uploaded:
                files_uploaded_item = files_uploaded_item_data.to_dict()

                files_uploaded.append(files_uploaded_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if device_id is not UNSET:
            field_dict["DeviceId"] = device_id
        if files_uploaded is not UNSET:
            field_dict["FilesUploaded"] = files_uploaded

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.devices_local_file_info import DevicesLocalFileInfo

        d = src_dict.copy()
        device_id = d.pop("DeviceId", UNSET)

        files_uploaded = []
        _files_uploaded = d.pop("FilesUploaded", UNSET)
        for files_uploaded_item_data in _files_uploaded or []:
            files_uploaded_item = DevicesLocalFileInfo.from_dict(files_uploaded_item_data)

            files_uploaded.append(files_uploaded_item)

        devices_content_upload_history = cls(
            device_id=device_id,
            files_uploaded=files_uploaded,
        )

        devices_content_upload_history.additional_properties = d
        return devices_content_upload_history

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
