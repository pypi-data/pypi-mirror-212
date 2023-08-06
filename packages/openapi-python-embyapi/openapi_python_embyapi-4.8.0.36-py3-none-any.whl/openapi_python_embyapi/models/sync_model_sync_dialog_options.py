from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.sync_model_sync_job_option import SyncModelSyncJobOption
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sync_model_sync_profile_option import SyncModelSyncProfileOption
    from ..models.sync_model_sync_quality_option import SyncModelSyncQualityOption
    from ..models.sync_sync_target import SyncSyncTarget


T = TypeVar("T", bound="SyncModelSyncDialogOptions")


@attr.s(auto_attribs=True)
class SyncModelSyncDialogOptions:
    """
    Attributes:
        targets (Union[Unset, List['SyncSyncTarget']]):
        options (Union[Unset, List[SyncModelSyncJobOption]]):
        quality_options (Union[Unset, List['SyncModelSyncQualityOption']]):
        profile_options (Union[Unset, List['SyncModelSyncProfileOption']]):
    """

    targets: Union[Unset, List["SyncSyncTarget"]] = UNSET
    options: Union[Unset, List[SyncModelSyncJobOption]] = UNSET
    quality_options: Union[Unset, List["SyncModelSyncQualityOption"]] = UNSET
    profile_options: Union[Unset, List["SyncModelSyncProfileOption"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        targets: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.targets, Unset):
            targets = []
            for targets_item_data in self.targets:
                targets_item = targets_item_data.to_dict()

                targets.append(targets_item)

        options: Union[Unset, List[str]] = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.value

                options.append(options_item)

        quality_options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.quality_options, Unset):
            quality_options = []
            for quality_options_item_data in self.quality_options:
                quality_options_item = quality_options_item_data.to_dict()

                quality_options.append(quality_options_item)

        profile_options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.profile_options, Unset):
            profile_options = []
            for profile_options_item_data in self.profile_options:
                profile_options_item = profile_options_item_data.to_dict()

                profile_options.append(profile_options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if targets is not UNSET:
            field_dict["Targets"] = targets
        if options is not UNSET:
            field_dict["Options"] = options
        if quality_options is not UNSET:
            field_dict["QualityOptions"] = quality_options
        if profile_options is not UNSET:
            field_dict["ProfileOptions"] = profile_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sync_model_sync_profile_option import SyncModelSyncProfileOption
        from ..models.sync_model_sync_quality_option import SyncModelSyncQualityOption
        from ..models.sync_sync_target import SyncSyncTarget

        d = src_dict.copy()
        targets = []
        _targets = d.pop("Targets", UNSET)
        for targets_item_data in _targets or []:
            targets_item = SyncSyncTarget.from_dict(targets_item_data)

            targets.append(targets_item)

        options = []
        _options = d.pop("Options", UNSET)
        for options_item_data in _options or []:
            options_item = SyncModelSyncJobOption(options_item_data)

            options.append(options_item)

        quality_options = []
        _quality_options = d.pop("QualityOptions", UNSET)
        for quality_options_item_data in _quality_options or []:
            quality_options_item = SyncModelSyncQualityOption.from_dict(quality_options_item_data)

            quality_options.append(quality_options_item)

        profile_options = []
        _profile_options = d.pop("ProfileOptions", UNSET)
        for profile_options_item_data in _profile_options or []:
            profile_options_item = SyncModelSyncProfileOption.from_dict(profile_options_item_data)

            profile_options.append(profile_options_item)

        sync_model_sync_dialog_options = cls(
            targets=targets,
            options=options,
            quality_options=quality_options,
            profile_options=profile_options,
        )

        sync_model_sync_dialog_options.additional_properties = d
        return sync_model_sync_dialog_options

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
