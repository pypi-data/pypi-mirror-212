from enum import Enum


class DrawingImageOrientation(str, Enum):
    BOTTOMLEFT = "BottomLeft"
    BOTTOMRIGHT = "BottomRight"
    LEFTBOTTOM = "LeftBottom"
    LEFTTOP = "LeftTop"
    RIGHTBOTTOM = "RightBottom"
    RIGHTTOP = "RightTop"
    TOPLEFT = "TopLeft"
    TOPRIGHT = "TopRight"

    def __str__(self) -> str:
        return str(self.value)
