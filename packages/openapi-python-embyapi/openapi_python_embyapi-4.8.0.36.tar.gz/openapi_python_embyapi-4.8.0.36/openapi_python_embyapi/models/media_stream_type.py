from enum import Enum


class MediaStreamType(str, Enum):
    ATTACHMENT = "Attachment"
    AUDIO = "Audio"
    DATA = "Data"
    EMBEDDEDIMAGE = "EmbeddedImage"
    SUBTITLE = "Subtitle"
    UNKNOWN = "Unknown"
    VIDEO = "Video"

    def __str__(self) -> str:
        return str(self.value)
