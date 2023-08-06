from enum import Enum


class SyncModelSyncJobOption(str, Enum):
    ITEMLIMIT = "ItemLimit"
    NAME = "Name"
    PROFILE = "Profile"
    QUALITY = "Quality"
    SYNCNEWCONTENT = "SyncNewContent"
    UNWATCHEDONLY = "UnwatchedOnly"

    def __str__(self) -> str:
        return str(self.value)
