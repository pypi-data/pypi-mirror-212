from enum import Enum


class PersonType(str, Enum):
    ACTOR = "Actor"
    COMPOSER = "Composer"
    CONDUCTOR = "Conductor"
    DIRECTOR = "Director"
    GUESTSTAR = "GuestStar"
    LYRICIST = "Lyricist"
    PRODUCER = "Producer"
    WRITER = "Writer"

    def __str__(self) -> str:
        return str(self.value)
