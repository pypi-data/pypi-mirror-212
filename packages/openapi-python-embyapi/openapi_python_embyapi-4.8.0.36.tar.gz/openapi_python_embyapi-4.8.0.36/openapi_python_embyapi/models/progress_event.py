from enum import Enum


class ProgressEvent(str, Enum):
    AUDIOTRACKCHANGE = "AudioTrackChange"
    PAUSE = "Pause"
    PLAYBACKRATECHANGE = "PlaybackRateChange"
    PLAYLISTITEMADD = "PlaylistItemAdd"
    PLAYLISTITEMMOVE = "PlaylistItemMove"
    PLAYLISTITEMREMOVE = "PlaylistItemRemove"
    QUALITYCHANGE = "QualityChange"
    REPEATMODECHANGE = "RepeatModeChange"
    STATECHANGE = "StateChange"
    SUBTITLEOFFSETCHANGE = "SubtitleOffsetChange"
    SUBTITLETRACKCHANGE = "SubtitleTrackChange"
    TIMEUPDATE = "TimeUpdate"
    UNPAUSE = "Unpause"
    VOLUMECHANGE = "VolumeChange"

    def __str__(self) -> str:
        return str(self.value)
