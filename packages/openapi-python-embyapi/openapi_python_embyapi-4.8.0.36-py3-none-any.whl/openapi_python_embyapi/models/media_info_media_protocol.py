from enum import Enum


class MediaInfoMediaProtocol(str, Enum):
    FILE = "File"
    FTP = "Ftp"
    HTTP = "Http"
    MMS = "Mms"
    RTMP = "Rtmp"
    RTP = "Rtp"
    RTSP = "Rtsp"
    UDP = "Udp"

    def __str__(self) -> str:
        return str(self.value)
