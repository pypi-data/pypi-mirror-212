from enum import Enum


class SyncModelItemFileType(str, Enum):
    IMAGE = "Image"
    MEDIA = "Media"
    SUBTITLES = "Subtitles"

    def __str__(self) -> str:
        return str(self.value)
