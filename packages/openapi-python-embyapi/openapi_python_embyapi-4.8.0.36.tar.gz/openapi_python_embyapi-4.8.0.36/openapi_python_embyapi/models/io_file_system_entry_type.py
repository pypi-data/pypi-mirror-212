from enum import Enum


class IOFileSystemEntryType(str, Enum):
    DIRECTORY = "Directory"
    FILE = "File"
    NETWORKCOMPUTER = "NetworkComputer"
    NETWORKSHARE = "NetworkShare"

    def __str__(self) -> str:
        return str(self.value)
