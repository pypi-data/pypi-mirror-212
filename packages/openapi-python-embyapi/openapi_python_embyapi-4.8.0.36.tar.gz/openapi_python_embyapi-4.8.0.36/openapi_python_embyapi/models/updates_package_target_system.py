from enum import Enum


class UpdatesPackageTargetSystem(str, Enum):
    MBCLASSIC = "MBClassic"
    MBTHEATER = "MBTheater"
    OTHER = "Other"
    SERVER = "Server"

    def __str__(self) -> str:
        return str(self.value)
