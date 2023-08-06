from enum import Enum


class SyncSyncCategory(str, Enum):
    LATEST = "Latest"
    NEXTUP = "NextUp"
    RESUME = "Resume"

    def __str__(self) -> str:
        return str(self.value)
