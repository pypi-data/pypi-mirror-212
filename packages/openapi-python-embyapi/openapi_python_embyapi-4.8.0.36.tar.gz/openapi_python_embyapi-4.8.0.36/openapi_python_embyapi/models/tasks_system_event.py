from enum import Enum


class TasksSystemEvent(str, Enum):
    DISPLAYCONFIGURATIONCHANGE = "DisplayConfigurationChange"
    NETWORKCHANGE = "NetworkChange"
    WAKEFROMSLEEP = "WakeFromSleep"

    def __str__(self) -> str:
        return str(self.value)
