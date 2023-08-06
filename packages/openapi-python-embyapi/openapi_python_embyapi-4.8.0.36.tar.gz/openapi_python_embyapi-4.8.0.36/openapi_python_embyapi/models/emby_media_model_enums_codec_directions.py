from enum import Enum


class EmbyMediaModelEnumsCodecDirections(str, Enum):
    DECODER = "Decoder"
    ENCODER = "Encoder"

    def __str__(self) -> str:
        return str(self.value)
