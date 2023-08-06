from enum import Enum


class EmbyWebGenericUIModelEnumsUICommandType(str, Enum):
    CUSTOM = "Custom"
    DIALOGCANCEL = "DialogCancel"
    DIALOGOK = "DialogOk"
    PAGEBACK = "PageBack"
    PAGESAVE = "PageSave"
    WIZARDBACK = "WizardBack"
    WIZARDBUTTON1 = "WizardButton1"
    WIZARDBUTTON2 = "WizardButton2"
    WIZARDBUTTON3 = "WizardButton3"
    WIZARDCANCEL = "WizardCancel"
    WIZARDFINISH = "WizardFinish"
    WIZARDNEXT = "WizardNext"

    def __str__(self) -> str:
        return str(self.value)
