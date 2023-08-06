from enum import Enum


class ConfigurationUnratedItem(str, Enum):
    BOOK = "Book"
    CHANNELCONTENT = "ChannelContent"
    GAME = "Game"
    LIVETVCHANNEL = "LiveTvChannel"
    LIVETVPROGRAM = "LiveTvProgram"
    MOVIE = "Movie"
    MUSIC = "Music"
    OTHER = "Other"
    SERIES = "Series"
    TRAILER = "Trailer"

    def __str__(self) -> str:
        return str(self.value)
