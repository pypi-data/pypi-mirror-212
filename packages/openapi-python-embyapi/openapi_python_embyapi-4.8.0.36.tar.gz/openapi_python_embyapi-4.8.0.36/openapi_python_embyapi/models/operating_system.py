from enum import Enum


class OperatingSystem(str, Enum):
    ANDROID = "Android"
    BSD = "BSD"
    LINUX = "Linux"
    OSX = "OSX"
    WINDOWS = "Windows"

    def __str__(self) -> str:
        return str(self.value)
