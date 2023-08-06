from enum import Enum


class PluginsConfigurationPageType(str, Enum):
    NONE = "None"
    PLUGINCONFIGURATION = "PluginConfiguration"

    def __str__(self) -> str:
        return str(self.value)
