from enum import Enum


class SyncSyncJobStatus(str, Enum):
    COMPLETED = "Completed"
    COMPLETEDWITHERROR = "CompletedWithError"
    CONVERTING = "Converting"
    FAILED = "Failed"
    QUEUED = "Queued"
    READYTOTRANSFER = "ReadyToTransfer"
    TRANSFERRING = "Transferring"

    def __str__(self) -> str:
        return str(self.value)
