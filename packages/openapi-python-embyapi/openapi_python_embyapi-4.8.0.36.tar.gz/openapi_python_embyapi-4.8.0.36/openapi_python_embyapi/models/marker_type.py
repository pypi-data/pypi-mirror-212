from enum import Enum


class MarkerType(str, Enum):
    CHAPTER = "Chapter"
    CREDITSSTART = "CreditsStart"
    INTROEND = "IntroEnd"
    INTROSTART = "IntroStart"

    def __str__(self) -> str:
        return str(self.value)
