from enum import Enum


class ImageType(str, Enum):
    ART = "Art"
    BACKDROP = "Backdrop"
    BANNER = "Banner"
    BOX = "Box"
    BOXREAR = "BoxRear"
    CHAPTER = "Chapter"
    DISC = "Disc"
    LOGO = "Logo"
    LOGOLIGHT = "LogoLight"
    LOGOLIGHTCOLOR = "LogoLightColor"
    MENU = "Menu"
    PRIMARY = "Primary"
    SCREENSHOT = "Screenshot"
    THUMB = "Thumb"
    THUMBNAIL = "Thumbnail"

    def __str__(self) -> str:
        return str(self.value)
