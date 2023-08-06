from enum import Enum


class EmbyMediaModelEnumsSecondaryFrameworks(str, Enum):
    AMDAMF = "AmdAmf"
    D3D11VA = "D3d11va"
    DXVA = "DxVa"
    MEDIACODEC = "MediaCodec"
    MMAL = "Mmal"
    NONE = "None"
    NVENCDEC = "NvEncDec"
    OPENMAX = "OpenMax"
    QUICKSYNC = "QuickSync"
    UNKNOWN = "Unknown"
    V4L2 = "V4L2"
    VAAPI = "VaApi"
    VIDEOTOOLBOX = "VideoToolbox"

    def __str__(self) -> str:
        return str(self.value)
