from enum import Enum


class EmbyWebGenericUIModelEnumsUIViewType(str, Enum):
    DIALOG = "Dialog"
    REGULARPAGE = "RegularPage"
    WIZARD = "Wizard"

    def __str__(self) -> str:
        return str(self.value)
