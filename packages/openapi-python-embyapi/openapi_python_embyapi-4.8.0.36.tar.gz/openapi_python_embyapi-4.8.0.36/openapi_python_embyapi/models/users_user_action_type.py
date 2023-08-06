from enum import Enum


class UsersUserActionType(str, Enum):
    PLAYEDITEM = "PlayedItem"

    def __str__(self) -> str:
        return str(self.value)
