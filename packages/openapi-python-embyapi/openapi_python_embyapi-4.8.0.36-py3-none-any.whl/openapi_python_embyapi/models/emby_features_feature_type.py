from enum import Enum


class EmbyFeaturesFeatureType(str, Enum):
    SYSTEM = "System"
    USER = "User"

    def __str__(self) -> str:
        return str(self.value)
