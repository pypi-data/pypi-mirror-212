from enum import Enum


class LiveTvKeywordType(str, Enum):
    ACTOR = "Actor"
    DIRECTOR = "Director"
    EPISODETITLE = "EpisodeTitle"
    NAME = "Name"
    OVERVIEW = "Overview"

    def __str__(self) -> str:
        return str(self.value)
