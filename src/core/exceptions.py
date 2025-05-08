import datetime
from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class ParserException(Exception):
    @property
    def message(self) -> str:
        return "Ошибка парсера!"


@dataclass(frozen=True, eq=False)
class StopDateException(ParserException):
    current_date: datetime.date
    stop_date: datetime.date

    @property
    def message(self) -> str:
        return f"Текущая дата {self.current_date} меньше даты остановки поиска {self.stop_date}!"
