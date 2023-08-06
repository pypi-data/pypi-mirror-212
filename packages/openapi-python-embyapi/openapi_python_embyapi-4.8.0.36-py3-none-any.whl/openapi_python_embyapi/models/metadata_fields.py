from enum import Enum


class MetadataFields(str, Enum):
    CAST = "Cast"
    CHANNELNUMBER = "ChannelNumber"
    COLLECTIONS = "Collections"
    COMMUNITYRATING = "CommunityRating"
    CRITICRATING = "CriticRating"
    GENRES = "Genres"
    NAME = "Name"
    OFFICIALRATING = "OfficialRating"
    ORIGINALTITLE = "OriginalTitle"
    OVERVIEW = "Overview"
    PRODUCTIONLOCATIONS = "ProductionLocations"
    RUNTIME = "Runtime"
    SORTINDEXNUMBER = "SortIndexNumber"
    SORTNAME = "SortName"
    SORTPARENTINDEXNUMBER = "SortParentIndexNumber"
    STUDIOS = "Studios"
    TAGLINE = "Tagline"
    TAGS = "Tags"

    def __str__(self) -> str:
        return str(self.value)
