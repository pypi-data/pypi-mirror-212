from enum import Enum


class ExtendedVideoTypes(str, Enum):
    DOLBYVISION = "DolbyVision"
    HDR10 = "Hdr10"
    HDR10PLUS = "Hdr10Plus"
    HYPERLOGGAMMA = "HyperLogGamma"
    NONE = "None"

    def __str__(self) -> str:
        return str(self.value)
