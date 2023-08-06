from enum import Enum


class ConfigurationSegmentSkipMode(str, Enum):
    AUTOSKIP = "AutoSkip"
    NONE = "None"
    SHOWBUTTON = "ShowButton"

    def __str__(self) -> str:
        return str(self.value)
