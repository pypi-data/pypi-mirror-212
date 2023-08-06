from enum import Enum


class ExtendedVideoSubTypes(str, Enum):
    DOVIPROFILE02 = "DoviProfile02"
    DOVIPROFILE10 = "DoviProfile10"
    DOVIPROFILE22 = "DoviProfile22"
    DOVIPROFILE30 = "DoviProfile30"
    DOVIPROFILE42 = "DoviProfile42"
    DOVIPROFILE50 = "DoviProfile50"
    DOVIPROFILE61 = "DoviProfile61"
    DOVIPROFILE76 = "DoviProfile76"
    DOVIPROFILE81 = "DoviProfile81"
    DOVIPROFILE82 = "DoviProfile82"
    DOVIPROFILE83 = "DoviProfile83"
    DOVIPROFILE84 = "DoviProfile84"
    DOVIPROFILE85 = "DoviProfile85"
    DOVIPROFILE92 = "DoviProfile92"
    HDR10 = "Hdr10"
    HDR10PLUS0 = "Hdr10Plus0"
    HYPERLOGGAMMA = "HyperLogGamma"
    NONE = "None"

    def __str__(self) -> str:
        return str(self.value)
