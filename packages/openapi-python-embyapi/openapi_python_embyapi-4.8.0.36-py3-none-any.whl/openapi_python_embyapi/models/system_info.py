from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.updates_package_version_class import UpdatesPackageVersionClass
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.updates_installation_info import UpdatesInstallationInfo


T = TypeVar("T", bound="SystemInfo")


@attr.s(auto_attribs=True)
class SystemInfo:
    """
    Attributes:
        system_update_level (Union[Unset, UpdatesPackageVersionClass]):
        operating_system_display_name (Union[Unset, str]):
        package_name (Union[Unset, str]):
        has_pending_restart (Union[Unset, bool]):
        is_shutting_down (Union[Unset, bool]):
        operating_system (Union[Unset, str]):
        supports_library_monitor (Union[Unset, bool]):
        supports_local_port_configuration (Union[Unset, bool]):
        supports_wake_server (Union[Unset, bool]):
        web_socket_port_number (Union[Unset, int]):
        completed_installations (Union[Unset, List['UpdatesInstallationInfo']]):
        can_self_restart (Union[Unset, bool]):
        can_self_update (Union[Unset, bool]):
        can_launch_web_browser (Union[Unset, bool]):
        program_data_path (Union[Unset, str]):
        items_by_name_path (Union[Unset, str]):
        cache_path (Union[Unset, str]):
        log_path (Union[Unset, str]):
        internal_metadata_path (Union[Unset, str]):
        transcoding_temp_path (Union[Unset, str]):
        http_server_port_number (Union[Unset, int]):
        supports_https (Union[Unset, bool]):
        https_port_number (Union[Unset, int]):
        has_update_available (Union[Unset, bool]):
        supports_auto_run_at_startup (Union[Unset, bool]):
        hardware_acceleration_requires_premiere (Union[Unset, bool]):
        local_address (Union[Unset, str]):
        local_addresses (Union[Unset, List[str]]):
        wan_address (Union[Unset, str]):
        remote_addresses (Union[Unset, List[str]]):
        server_name (Union[Unset, str]):
        version (Union[Unset, str]):
        id (Union[Unset, str]):
    """

    system_update_level: Union[Unset, UpdatesPackageVersionClass] = UNSET
    operating_system_display_name: Union[Unset, str] = UNSET
    package_name: Union[Unset, str] = UNSET
    has_pending_restart: Union[Unset, bool] = UNSET
    is_shutting_down: Union[Unset, bool] = UNSET
    operating_system: Union[Unset, str] = UNSET
    supports_library_monitor: Union[Unset, bool] = UNSET
    supports_local_port_configuration: Union[Unset, bool] = UNSET
    supports_wake_server: Union[Unset, bool] = UNSET
    web_socket_port_number: Union[Unset, int] = UNSET
    completed_installations: Union[Unset, List["UpdatesInstallationInfo"]] = UNSET
    can_self_restart: Union[Unset, bool] = UNSET
    can_self_update: Union[Unset, bool] = UNSET
    can_launch_web_browser: Union[Unset, bool] = UNSET
    program_data_path: Union[Unset, str] = UNSET
    items_by_name_path: Union[Unset, str] = UNSET
    cache_path: Union[Unset, str] = UNSET
    log_path: Union[Unset, str] = UNSET
    internal_metadata_path: Union[Unset, str] = UNSET
    transcoding_temp_path: Union[Unset, str] = UNSET
    http_server_port_number: Union[Unset, int] = UNSET
    supports_https: Union[Unset, bool] = UNSET
    https_port_number: Union[Unset, int] = UNSET
    has_update_available: Union[Unset, bool] = UNSET
    supports_auto_run_at_startup: Union[Unset, bool] = UNSET
    hardware_acceleration_requires_premiere: Union[Unset, bool] = UNSET
    local_address: Union[Unset, str] = UNSET
    local_addresses: Union[Unset, List[str]] = UNSET
    wan_address: Union[Unset, str] = UNSET
    remote_addresses: Union[Unset, List[str]] = UNSET
    server_name: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        system_update_level: Union[Unset, str] = UNSET
        if not isinstance(self.system_update_level, Unset):
            system_update_level = self.system_update_level.value

        operating_system_display_name = self.operating_system_display_name
        package_name = self.package_name
        has_pending_restart = self.has_pending_restart
        is_shutting_down = self.is_shutting_down
        operating_system = self.operating_system
        supports_library_monitor = self.supports_library_monitor
        supports_local_port_configuration = self.supports_local_port_configuration
        supports_wake_server = self.supports_wake_server
        web_socket_port_number = self.web_socket_port_number
        completed_installations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.completed_installations, Unset):
            completed_installations = []
            for completed_installations_item_data in self.completed_installations:
                completed_installations_item = completed_installations_item_data.to_dict()

                completed_installations.append(completed_installations_item)

        can_self_restart = self.can_self_restart
        can_self_update = self.can_self_update
        can_launch_web_browser = self.can_launch_web_browser
        program_data_path = self.program_data_path
        items_by_name_path = self.items_by_name_path
        cache_path = self.cache_path
        log_path = self.log_path
        internal_metadata_path = self.internal_metadata_path
        transcoding_temp_path = self.transcoding_temp_path
        http_server_port_number = self.http_server_port_number
        supports_https = self.supports_https
        https_port_number = self.https_port_number
        has_update_available = self.has_update_available
        supports_auto_run_at_startup = self.supports_auto_run_at_startup
        hardware_acceleration_requires_premiere = self.hardware_acceleration_requires_premiere
        local_address = self.local_address
        local_addresses: Union[Unset, List[str]] = UNSET
        if not isinstance(self.local_addresses, Unset):
            local_addresses = self.local_addresses

        wan_address = self.wan_address
        remote_addresses: Union[Unset, List[str]] = UNSET
        if not isinstance(self.remote_addresses, Unset):
            remote_addresses = self.remote_addresses

        server_name = self.server_name
        version = self.version
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if system_update_level is not UNSET:
            field_dict["SystemUpdateLevel"] = system_update_level
        if operating_system_display_name is not UNSET:
            field_dict["OperatingSystemDisplayName"] = operating_system_display_name
        if package_name is not UNSET:
            field_dict["PackageName"] = package_name
        if has_pending_restart is not UNSET:
            field_dict["HasPendingRestart"] = has_pending_restart
        if is_shutting_down is not UNSET:
            field_dict["IsShuttingDown"] = is_shutting_down
        if operating_system is not UNSET:
            field_dict["OperatingSystem"] = operating_system
        if supports_library_monitor is not UNSET:
            field_dict["SupportsLibraryMonitor"] = supports_library_monitor
        if supports_local_port_configuration is not UNSET:
            field_dict["SupportsLocalPortConfiguration"] = supports_local_port_configuration
        if supports_wake_server is not UNSET:
            field_dict["SupportsWakeServer"] = supports_wake_server
        if web_socket_port_number is not UNSET:
            field_dict["WebSocketPortNumber"] = web_socket_port_number
        if completed_installations is not UNSET:
            field_dict["CompletedInstallations"] = completed_installations
        if can_self_restart is not UNSET:
            field_dict["CanSelfRestart"] = can_self_restart
        if can_self_update is not UNSET:
            field_dict["CanSelfUpdate"] = can_self_update
        if can_launch_web_browser is not UNSET:
            field_dict["CanLaunchWebBrowser"] = can_launch_web_browser
        if program_data_path is not UNSET:
            field_dict["ProgramDataPath"] = program_data_path
        if items_by_name_path is not UNSET:
            field_dict["ItemsByNamePath"] = items_by_name_path
        if cache_path is not UNSET:
            field_dict["CachePath"] = cache_path
        if log_path is not UNSET:
            field_dict["LogPath"] = log_path
        if internal_metadata_path is not UNSET:
            field_dict["InternalMetadataPath"] = internal_metadata_path
        if transcoding_temp_path is not UNSET:
            field_dict["TranscodingTempPath"] = transcoding_temp_path
        if http_server_port_number is not UNSET:
            field_dict["HttpServerPortNumber"] = http_server_port_number
        if supports_https is not UNSET:
            field_dict["SupportsHttps"] = supports_https
        if https_port_number is not UNSET:
            field_dict["HttpsPortNumber"] = https_port_number
        if has_update_available is not UNSET:
            field_dict["HasUpdateAvailable"] = has_update_available
        if supports_auto_run_at_startup is not UNSET:
            field_dict["SupportsAutoRunAtStartup"] = supports_auto_run_at_startup
        if hardware_acceleration_requires_premiere is not UNSET:
            field_dict["HardwareAccelerationRequiresPremiere"] = hardware_acceleration_requires_premiere
        if local_address is not UNSET:
            field_dict["LocalAddress"] = local_address
        if local_addresses is not UNSET:
            field_dict["LocalAddresses"] = local_addresses
        if wan_address is not UNSET:
            field_dict["WanAddress"] = wan_address
        if remote_addresses is not UNSET:
            field_dict["RemoteAddresses"] = remote_addresses
        if server_name is not UNSET:
            field_dict["ServerName"] = server_name
        if version is not UNSET:
            field_dict["Version"] = version
        if id is not UNSET:
            field_dict["Id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.updates_installation_info import UpdatesInstallationInfo

        d = src_dict.copy()
        _system_update_level = d.pop("SystemUpdateLevel", UNSET)
        system_update_level: Union[Unset, UpdatesPackageVersionClass]
        if isinstance(_system_update_level, Unset):
            system_update_level = UNSET
        else:
            system_update_level = UpdatesPackageVersionClass(_system_update_level)

        operating_system_display_name = d.pop("OperatingSystemDisplayName", UNSET)

        package_name = d.pop("PackageName", UNSET)

        has_pending_restart = d.pop("HasPendingRestart", UNSET)

        is_shutting_down = d.pop("IsShuttingDown", UNSET)

        operating_system = d.pop("OperatingSystem", UNSET)

        supports_library_monitor = d.pop("SupportsLibraryMonitor", UNSET)

        supports_local_port_configuration = d.pop("SupportsLocalPortConfiguration", UNSET)

        supports_wake_server = d.pop("SupportsWakeServer", UNSET)

        web_socket_port_number = d.pop("WebSocketPortNumber", UNSET)

        completed_installations = []
        _completed_installations = d.pop("CompletedInstallations", UNSET)
        for completed_installations_item_data in _completed_installations or []:
            completed_installations_item = UpdatesInstallationInfo.from_dict(completed_installations_item_data)

            completed_installations.append(completed_installations_item)

        can_self_restart = d.pop("CanSelfRestart", UNSET)

        can_self_update = d.pop("CanSelfUpdate", UNSET)

        can_launch_web_browser = d.pop("CanLaunchWebBrowser", UNSET)

        program_data_path = d.pop("ProgramDataPath", UNSET)

        items_by_name_path = d.pop("ItemsByNamePath", UNSET)

        cache_path = d.pop("CachePath", UNSET)

        log_path = d.pop("LogPath", UNSET)

        internal_metadata_path = d.pop("InternalMetadataPath", UNSET)

        transcoding_temp_path = d.pop("TranscodingTempPath", UNSET)

        http_server_port_number = d.pop("HttpServerPortNumber", UNSET)

        supports_https = d.pop("SupportsHttps", UNSET)

        https_port_number = d.pop("HttpsPortNumber", UNSET)

        has_update_available = d.pop("HasUpdateAvailable", UNSET)

        supports_auto_run_at_startup = d.pop("SupportsAutoRunAtStartup", UNSET)

        hardware_acceleration_requires_premiere = d.pop("HardwareAccelerationRequiresPremiere", UNSET)

        local_address = d.pop("LocalAddress", UNSET)

        local_addresses = cast(List[str], d.pop("LocalAddresses", UNSET))

        wan_address = d.pop("WanAddress", UNSET)

        remote_addresses = cast(List[str], d.pop("RemoteAddresses", UNSET))

        server_name = d.pop("ServerName", UNSET)

        version = d.pop("Version", UNSET)

        id = d.pop("Id", UNSET)

        system_info = cls(
            system_update_level=system_update_level,
            operating_system_display_name=operating_system_display_name,
            package_name=package_name,
            has_pending_restart=has_pending_restart,
            is_shutting_down=is_shutting_down,
            operating_system=operating_system,
            supports_library_monitor=supports_library_monitor,
            supports_local_port_configuration=supports_local_port_configuration,
            supports_wake_server=supports_wake_server,
            web_socket_port_number=web_socket_port_number,
            completed_installations=completed_installations,
            can_self_restart=can_self_restart,
            can_self_update=can_self_update,
            can_launch_web_browser=can_launch_web_browser,
            program_data_path=program_data_path,
            items_by_name_path=items_by_name_path,
            cache_path=cache_path,
            log_path=log_path,
            internal_metadata_path=internal_metadata_path,
            transcoding_temp_path=transcoding_temp_path,
            http_server_port_number=http_server_port_number,
            supports_https=supports_https,
            https_port_number=https_port_number,
            has_update_available=has_update_available,
            supports_auto_run_at_startup=supports_auto_run_at_startup,
            hardware_acceleration_requires_premiere=hardware_acceleration_requires_premiere,
            local_address=local_address,
            local_addresses=local_addresses,
            wan_address=wan_address,
            remote_addresses=remote_addresses,
            server_name=server_name,
            version=version,
            id=id,
        )

        system_info.additional_properties = d
        return system_info

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
