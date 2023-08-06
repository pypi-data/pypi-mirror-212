from enum import Enum


class LoggingLogSeverity(str, Enum):
    DEBUG = "Debug"
    ERROR = "Error"
    FATAL = "Fatal"
    INFO = "Info"
    WARN = "Warn"

    def __str__(self) -> str:
        return str(self.value)
