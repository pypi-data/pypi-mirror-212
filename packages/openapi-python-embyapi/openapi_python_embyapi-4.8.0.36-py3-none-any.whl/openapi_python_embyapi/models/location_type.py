from enum import Enum


class LocationType(str, Enum):
    FILESYSTEM = "FileSystem"
    VIRTUAL = "Virtual"

    def __str__(self) -> str:
        return str(self.value)
