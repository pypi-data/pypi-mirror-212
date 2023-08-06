from enum import Enum


class LiveTvTimerType(str, Enum):
    DATETIME = "DateTime"
    KEYWORD = "Keyword"
    PROGRAM = "Program"

    def __str__(self) -> str:
        return str(self.value)
