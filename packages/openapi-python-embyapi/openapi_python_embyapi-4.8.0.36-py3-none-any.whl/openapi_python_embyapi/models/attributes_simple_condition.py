from enum import Enum


class AttributesSimpleCondition(str, Enum):
    ISFALSE = "IsFalse"
    ISNOTNULLOREMPTY = "IsNotNullOrEmpty"
    ISNULL = "IsNull"
    ISTRUE = "IsTrue"

    def __str__(self) -> str:
        return str(self.value)
