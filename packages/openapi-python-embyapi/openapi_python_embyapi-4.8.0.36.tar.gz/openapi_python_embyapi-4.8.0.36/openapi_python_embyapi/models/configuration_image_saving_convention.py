from enum import Enum


class ConfigurationImageSavingConvention(str, Enum):
    COMPATIBLE = "Compatible"
    LEGACY = "Legacy"

    def __str__(self) -> str:
        return str(self.value)
