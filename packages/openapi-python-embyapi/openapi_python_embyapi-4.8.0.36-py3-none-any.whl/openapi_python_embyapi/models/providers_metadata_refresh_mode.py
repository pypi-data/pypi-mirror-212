from enum import Enum


class ProvidersMetadataRefreshMode(str, Enum):
    DEFAULT = "Default"
    FULLREFRESH = "FullRefresh"
    VALIDATIONONLY = "ValidationOnly"

    def __str__(self) -> str:
        return str(self.value)
