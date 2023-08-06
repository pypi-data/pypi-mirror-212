from enum import Enum


class UpdatesPackageVersionClass(str, Enum):
    BETA = "Beta"
    DEV = "Dev"
    RELEASE = "Release"

    def __str__(self) -> str:
        return str(self.value)
