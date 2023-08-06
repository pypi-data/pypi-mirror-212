from enum import Enum


class TasksTaskCompletionStatus(str, Enum):
    ABORTED = "Aborted"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    FAILED = "Failed"

    def __str__(self) -> str:
        return str(self.value)
