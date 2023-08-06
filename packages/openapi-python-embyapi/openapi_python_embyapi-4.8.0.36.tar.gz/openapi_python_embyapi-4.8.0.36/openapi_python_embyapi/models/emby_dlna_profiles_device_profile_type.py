from enum import Enum


class EmbyDlnaProfilesDeviceProfileType(str, Enum):
    SYSTEM = "System"
    USER = "User"

    def __str__(self) -> str:
        return str(self.value)
