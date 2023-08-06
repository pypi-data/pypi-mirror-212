from enum import Enum


class EmbyWebGenericEditConditionsPropertyConditionType(str, Enum):
    ENABLED = "Enabled"
    VISIBLE = "Visible"

    def __str__(self) -> str:
        return str(self.value)
