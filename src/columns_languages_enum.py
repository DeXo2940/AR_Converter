import enum


class AbstractColumns(enum.Enum):
    pass


class ColumnsPL(AbstractColumns):
    EMPLOYEE = "Pracownik"
    DATE = "Data"
    TASK_GROUP = "Grupa zadań"
    TASK = "Zadanie"
    DESCRIPTION = "Opis"
    TIME = "Czas"


class ColumnsEN(AbstractColumns):
    EMPLOYEE = "Employee"
    DATE = "Date"
    TASK_GROUP = "Task group"
    TASK = "Task"
    DESCRIPTION = "Description"
    TIME = "Reporting duration"
