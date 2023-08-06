from enum import Enum


class DlnaPlaybackErrorCode(str, Enum):
    NOCOMPATIBLESTREAM = "NoCompatibleStream"
    NOTALLOWED = "NotAllowed"
    RATELIMITEXCEEDED = "RateLimitExceeded"

    def __str__(self) -> str:
        return str(self.value)
