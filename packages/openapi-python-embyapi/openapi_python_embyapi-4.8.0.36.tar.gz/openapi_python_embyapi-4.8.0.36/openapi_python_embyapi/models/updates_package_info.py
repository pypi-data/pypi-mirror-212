import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.updates_package_target_system import UpdatesPackageTargetSystem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.updates_package_version_info import UpdatesPackageVersionInfo


T = TypeVar("T", bound="UpdatesPackageInfo")


@attr.s(auto_attribs=True)
class UpdatesPackageInfo:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        short_description (Union[Unset, str]):
        overview (Union[Unset, str]):
        is_premium (Union[Unset, bool]):
        adult (Union[Unset, bool]):
        rich_desc_url (Union[Unset, str]):
        thumb_image (Union[Unset, str]):
        preview_image (Union[Unset, str]):
        type (Union[Unset, str]):
        target_filename (Union[Unset, str]):
        owner (Union[Unset, str]):
        category (Union[Unset, str]):
        tile_color (Union[Unset, str]):
        feature_id (Union[Unset, str]):
        price (Union[Unset, None, float]):
        target_system (Union[Unset, UpdatesPackageTargetSystem]):
        guid (Union[Unset, str]):
        is_registered (Union[Unset, bool]):
        exp_date (Union[Unset, datetime.datetime]):
        versions (Union[Unset, List['UpdatesPackageVersionInfo']]):
        enable_in_app_store (Union[Unset, bool]):
        installs (Union[Unset, int]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    short_description: Union[Unset, str] = UNSET
    overview: Union[Unset, str] = UNSET
    is_premium: Union[Unset, bool] = UNSET
    adult: Union[Unset, bool] = UNSET
    rich_desc_url: Union[Unset, str] = UNSET
    thumb_image: Union[Unset, str] = UNSET
    preview_image: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    target_filename: Union[Unset, str] = UNSET
    owner: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    tile_color: Union[Unset, str] = UNSET
    feature_id: Union[Unset, str] = UNSET
    price: Union[Unset, None, float] = UNSET
    target_system: Union[Unset, UpdatesPackageTargetSystem] = UNSET
    guid: Union[Unset, str] = UNSET
    is_registered: Union[Unset, bool] = UNSET
    exp_date: Union[Unset, datetime.datetime] = UNSET
    versions: Union[Unset, List["UpdatesPackageVersionInfo"]] = UNSET
    enable_in_app_store: Union[Unset, bool] = UNSET
    installs: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        short_description = self.short_description
        overview = self.overview
        is_premium = self.is_premium
        adult = self.adult
        rich_desc_url = self.rich_desc_url
        thumb_image = self.thumb_image
        preview_image = self.preview_image
        type = self.type
        target_filename = self.target_filename
        owner = self.owner
        category = self.category
        tile_color = self.tile_color
        feature_id = self.feature_id
        price = self.price
        target_system: Union[Unset, str] = UNSET
        if not isinstance(self.target_system, Unset):
            target_system = self.target_system.value

        guid = self.guid
        is_registered = self.is_registered
        exp_date: Union[Unset, str] = UNSET
        if not isinstance(self.exp_date, Unset):
            exp_date = self.exp_date.isoformat()

        versions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.versions, Unset):
            versions = []
            for versions_item_data in self.versions:
                versions_item = versions_item_data.to_dict()

                versions.append(versions_item)

        enable_in_app_store = self.enable_in_app_store
        installs = self.installs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if short_description is not UNSET:
            field_dict["shortDescription"] = short_description
        if overview is not UNSET:
            field_dict["overview"] = overview
        if is_premium is not UNSET:
            field_dict["isPremium"] = is_premium
        if adult is not UNSET:
            field_dict["adult"] = adult
        if rich_desc_url is not UNSET:
            field_dict["richDescUrl"] = rich_desc_url
        if thumb_image is not UNSET:
            field_dict["thumbImage"] = thumb_image
        if preview_image is not UNSET:
            field_dict["previewImage"] = preview_image
        if type is not UNSET:
            field_dict["type"] = type
        if target_filename is not UNSET:
            field_dict["targetFilename"] = target_filename
        if owner is not UNSET:
            field_dict["owner"] = owner
        if category is not UNSET:
            field_dict["category"] = category
        if tile_color is not UNSET:
            field_dict["tileColor"] = tile_color
        if feature_id is not UNSET:
            field_dict["featureId"] = feature_id
        if price is not UNSET:
            field_dict["price"] = price
        if target_system is not UNSET:
            field_dict["targetSystem"] = target_system
        if guid is not UNSET:
            field_dict["guid"] = guid
        if is_registered is not UNSET:
            field_dict["isRegistered"] = is_registered
        if exp_date is not UNSET:
            field_dict["expDate"] = exp_date
        if versions is not UNSET:
            field_dict["versions"] = versions
        if enable_in_app_store is not UNSET:
            field_dict["enableInAppStore"] = enable_in_app_store
        if installs is not UNSET:
            field_dict["installs"] = installs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.updates_package_version_info import UpdatesPackageVersionInfo

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        short_description = d.pop("shortDescription", UNSET)

        overview = d.pop("overview", UNSET)

        is_premium = d.pop("isPremium", UNSET)

        adult = d.pop("adult", UNSET)

        rich_desc_url = d.pop("richDescUrl", UNSET)

        thumb_image = d.pop("thumbImage", UNSET)

        preview_image = d.pop("previewImage", UNSET)

        type = d.pop("type", UNSET)

        target_filename = d.pop("targetFilename", UNSET)

        owner = d.pop("owner", UNSET)

        category = d.pop("category", UNSET)

        tile_color = d.pop("tileColor", UNSET)

        feature_id = d.pop("featureId", UNSET)

        price = d.pop("price", UNSET)

        _target_system = d.pop("targetSystem", UNSET)
        target_system: Union[Unset, UpdatesPackageTargetSystem]
        if isinstance(_target_system, Unset):
            target_system = UNSET
        else:
            target_system = UpdatesPackageTargetSystem(_target_system)

        guid = d.pop("guid", UNSET)

        is_registered = d.pop("isRegistered", UNSET)

        _exp_date = d.pop("expDate", UNSET)
        exp_date: Union[Unset, datetime.datetime]
        if isinstance(_exp_date, Unset):
            exp_date = UNSET
        else:
            exp_date = isoparse(_exp_date)

        versions = []
        _versions = d.pop("versions", UNSET)
        for versions_item_data in _versions or []:
            versions_item = UpdatesPackageVersionInfo.from_dict(versions_item_data)

            versions.append(versions_item)

        enable_in_app_store = d.pop("enableInAppStore", UNSET)

        installs = d.pop("installs", UNSET)

        updates_package_info = cls(
            id=id,
            name=name,
            short_description=short_description,
            overview=overview,
            is_premium=is_premium,
            adult=adult,
            rich_desc_url=rich_desc_url,
            thumb_image=thumb_image,
            preview_image=preview_image,
            type=type,
            target_filename=target_filename,
            owner=owner,
            category=category,
            tile_color=tile_color,
            feature_id=feature_id,
            price=price,
            target_system=target_system,
            guid=guid,
            is_registered=is_registered,
            exp_date=exp_date,
            versions=versions,
            enable_in_app_store=enable_in_app_store,
            installs=installs,
        )

        updates_package_info.additional_properties = d
        return updates_package_info

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
