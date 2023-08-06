from enum import Enum


class EmbyMediaModelEnumsCodecKinds(str, Enum):
    AUDIO = "Audio"
    SUBTITLES = "SubTitles"
    VIDEO = "Video"

    def __str__(self) -> str:
        return str(self.value)
