from enum import Enum


class AttributesValueCondition(str, Enum):
    ISEQUAL = "IsEqual"
    ISGREATER = "IsGreater"
    ISGREATEROREQUAL = "IsGreaterOrEqual"
    ISLESS = "IsLess"
    ISLESSOREQUAL = "IsLessOrEqual"
    ISNOTEQUAL = "IsNotEqual"

    def __str__(self) -> str:
        return str(self.value)
