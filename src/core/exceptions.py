import datetime
from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class ParserException(Exception):
    @property
    def message(self) -> str:
        return "Ошибка парсера!"


@dataclass(frozen=True, eq=False)
class TableNotFoundException(ParserException):
    table_title: str

    @property
    def message(self) -> str:
        return f"Таблица с названием '{self.table_title}' не найдена!"


@dataclass(frozen=True, eq=False)
class PageNotLoadedException(ParserException):
    url: str

    @property
    def message(self) -> str:
        return f"Страница по адресу: '{self.url}' не загружена!"


@dataclass(frozen=True, eq=False)
class FileNotLoadedException(ParserException):
    file_link: str

    @property
    def message(self) -> str:
        return f"Файл не был загружен по ссылке: '{self.file_link}'!"
