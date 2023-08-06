from enum import Enum


class DlnaSubtitleDeliveryMethod(str, Enum):
    EMBED = "Embed"
    ENCODE = "Encode"
    EXTERNAL = "External"
    HLS = "Hls"
    VIDEOSIDEDATA = "VideoSideData"

    def __str__(self) -> str:
        return str(self.value)
