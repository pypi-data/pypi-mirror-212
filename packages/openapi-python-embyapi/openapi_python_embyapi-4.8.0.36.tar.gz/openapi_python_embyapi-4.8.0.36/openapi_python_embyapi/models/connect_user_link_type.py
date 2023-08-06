from enum import Enum


class ConnectUserLinkType(str, Enum):
    GUEST = "Guest"
    LINKEDUSER = "LinkedUser"

    def __str__(self) -> str:
        return str(self.value)
