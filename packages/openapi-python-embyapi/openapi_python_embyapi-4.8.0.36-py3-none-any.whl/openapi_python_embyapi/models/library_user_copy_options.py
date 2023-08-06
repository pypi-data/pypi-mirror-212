from enum import Enum


class LibraryUserCopyOptions(str, Enum):
    USERCONFIGURATION = "UserConfiguration"
    USERPOLICY = "UserPolicy"

    def __str__(self) -> str:
        return str(self.value)
