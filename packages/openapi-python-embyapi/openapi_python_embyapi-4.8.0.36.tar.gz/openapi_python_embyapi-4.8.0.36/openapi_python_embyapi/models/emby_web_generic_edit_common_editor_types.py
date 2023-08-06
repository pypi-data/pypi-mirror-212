from enum import Enum


class EmbyWebGenericEditCommonEditorTypes(str, Enum):
    BOOLEAN = "Boolean"
    BUTTONGROUP = "ButtonGroup"
    BUTTONITEM = "ButtonItem"
    CAPTIONITEM = "CaptionItem"
    DATE = "Date"
    DXDATAGRID = "DxDataGrid"
    DXPIVOTGRID = "DxPivotGrid"
    FILEPATH = "FilePath"
    FOLDERPATH = "FolderPath"
    GROUP = "Group"
    ITEMLIST = "ItemList"
    LABELITEM = "LabelItem"
    NUMERIC = "Numeric"
    PROGRESSITEM = "ProgressItem"
    RADIOGROUP = "RadioGroup"
    SELECTMULTIPLE = "SelectMultiple"
    SELECTSINGLE = "SelectSingle"
    SPACERITEM = "SpacerItem"
    STATUSITEM = "StatusItem"
    TEXT = "Text"

    def __str__(self) -> str:
        return str(self.value)
