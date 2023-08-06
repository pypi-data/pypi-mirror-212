from enum import Enum


class EmbyDlnaProfilesHeaderMatchType(str, Enum):
    EQUALS = "Equals"
    REGEX = "Regex"
    SUBSTRING = "Substring"

    def __str__(self) -> str:
        return str(self.value)
