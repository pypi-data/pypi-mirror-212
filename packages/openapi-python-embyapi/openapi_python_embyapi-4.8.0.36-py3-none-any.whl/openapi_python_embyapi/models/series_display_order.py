from enum import Enum


class SeriesDisplayOrder(str, Enum):
    ABSOLUTE = "Absolute"
    AIRED = "Aired"
    DVD = "Dvd"

    def __str__(self) -> str:
        return str(self.value)
