from enum import Enum


class SubtitleLocationType(str, Enum):
    INTERNALSTREAM = "InternalStream"
    VIDEOSIDEDATA = "VideoSideData"

    def __str__(self) -> str:
        return str(self.value)
