from enum import Enum


class SyncModelSyncJobItemStatus(str, Enum):
    CONVERTING = "Converting"
    FAILED = "Failed"
    QUEUED = "Queued"
    READYTOTRANSFER = "ReadyToTransfer"
    SYNCED = "Synced"
    TRANSFERRING = "Transferring"

    def __str__(self) -> str:
        return str(self.value)
