from enum import Enum


class LibraryItemLinkType(str, Enum):
    ALBUMARTISTS = "AlbumArtists"
    ALBUMS = "Albums"
    ARTISTS = "Artists"
    COLLECTIONFOLDERS = "CollectionFolders"
    COLLECTIONS = "Collections"
    COMPOSERS = "Composers"
    GENRES = "Genres"
    STUDIOS = "Studios"
    TAGS = "Tags"

    def __str__(self) -> str:
        return str(self.value)
