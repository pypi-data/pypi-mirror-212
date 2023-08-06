from enum import Enum


class TranscodingVpStepTypes(str, Enum):
    BURNINGRAPHICSUBS = "BurnInGraphicSubs"
    BURNINTEXTSUBS = "BurnInTextSubs"
    CENSOR = "Censor"
    COLORCONVERSION = "ColorConversion"
    CONNECTTO = "ConnectTo"
    DECODER = "Decoder"
    DEINTERLACE = "Deinterlace"
    ENCODER = "Encoder"
    GRAPHICSUB2TEXT = "GraphicSub2Text"
    GRAPHICSUB2VIDEO = "GraphicSub2Video"
    SCALESUBS = "ScaleSubs"
    SCALING = "Scaling"
    SHOWSPEAKER = "ShowSpeaker"
    SPLITCAPTIONS = "SplitCaptions"
    STRIPSTYLES = "StripStyles"
    SUBTITLEOVERLAY = "SubtitleOverlay"
    TEXTMOD = "TextMod"
    TEXTSUB2VIDEO = "TextSub2Video"
    TONEMAPPING = "ToneMapping"

    def __str__(self) -> str:
        return str(self.value)
