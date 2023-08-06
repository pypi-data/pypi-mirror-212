from enum import Enum


class ConfigurationMetadataFeatures(str, Enum):
    ADULT = "Adult"
    COLLECTIONS = "Collections"
    REQUIREDSETUP = "RequiredSetup"

    def __str__(self) -> str:
        return str(self.value)
