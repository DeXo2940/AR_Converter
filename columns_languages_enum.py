from enum import Enum


class AbstractColumns(Enum):
    pass


class ColumnsPL(AbstractColumns):
    DATE = "Data"
    TASK_GROUP = "Grupa zadań"
    TASK = "Zadanie"
    DESCRIPTION = "Opis"
    TIME = "Czas"


class ColumnsEN(AbstractColumns):
    DATE = "Date"
    TASK_GROUP = "Task group"
    TASK = "Task"
    DESCRIPTION = "Description"
    TIME = "Reporting duration"
