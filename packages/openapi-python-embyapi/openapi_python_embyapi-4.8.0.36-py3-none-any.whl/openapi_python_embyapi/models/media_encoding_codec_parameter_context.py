from enum import Enum


class MediaEncodingCodecParameterContext(str, Enum):
    CONVERSION = "Conversion"
    PLAYBACK = "Playback"

    def __str__(self) -> str:
        return str(self.value)
