from enum import Enum


class TranscodeReason(str, Enum):
    ANAMORPHICVIDEONOTSUPPORTED = "AnamorphicVideoNotSupported"
    AUDIOBITDEPTHNOTSUPPORTED = "AudioBitDepthNotSupported"
    AUDIOBITRATENOTSUPPORTED = "AudioBitrateNotSupported"
    AUDIOCHANNELSNOTSUPPORTED = "AudioChannelsNotSupported"
    AUDIOCODECNOTSUPPORTED = "AudioCodecNotSupported"
    AUDIOPROFILENOTSUPPORTED = "AudioProfileNotSupported"
    AUDIOSAMPLERATENOTSUPPORTED = "AudioSampleRateNotSupported"
    CONTAINERBITRATEEXCEEDSLIMIT = "ContainerBitrateExceedsLimit"
    CONTAINERNOTSUPPORTED = "ContainerNotSupported"
    DIRECTPLAYERROR = "DirectPlayError"
    INTERLACEDVIDEONOTSUPPORTED = "InterlacedVideoNotSupported"
    REFFRAMESNOTSUPPORTED = "RefFramesNotSupported"
    SECONDARYAUDIONOTSUPPORTED = "SecondaryAudioNotSupported"
    SUBTITLECODECNOTSUPPORTED = "SubtitleCodecNotSupported"
    SUBTITLECONTENTOPTIONSENABLED = "SubtitleContentOptionsEnabled"
    UNKNOWNAUDIOSTREAMINFO = "UnknownAudioStreamInfo"
    UNKNOWNVIDEOSTREAMINFO = "UnknownVideoStreamInfo"
    VIDEOBITDEPTHNOTSUPPORTED = "VideoBitDepthNotSupported"
    VIDEOBITRATENOTSUPPORTED = "VideoBitrateNotSupported"
    VIDEOCODECNOTSUPPORTED = "VideoCodecNotSupported"
    VIDEOFRAMERATENOTSUPPORTED = "VideoFramerateNotSupported"
    VIDEOLEVELNOTSUPPORTED = "VideoLevelNotSupported"
    VIDEOPROFILENOTSUPPORTED = "VideoProfileNotSupported"
    VIDEORANGENOTSUPPORTED = "VideoRangeNotSupported"
    VIDEORESOLUTIONNOTSUPPORTED = "VideoResolutionNotSupported"

    def __str__(self) -> str:
        return str(self.value)
