from dataclasses import dataclass, field
from typing import runtime_checkable, Protocol

from .file_db import JSONSaverFile
from ..configs import DBConfig
from ..entity import FileConfig


__all__ = ["Repository"]


@runtime_checkable
class VacancySaverInterface(Protocol):
    """
    Saving data interface.
    """

    def add_vacancy(self, vacancy: list | dict) -> None:
        ...

    def get_vacancies_by_salary(self, salary_min: int) -> list:
        ...

    def delete_vacancy(self, vacancy_url: str) -> None:
        ...


@dataclass
class Repository:
    """
    DataBase repository.
    """

    db: VacancySaverInterface = field(init=False)
    cfg: DBConfig

    def __post_init__(self) -> None:
        self._db_selection()

    def _db_selection(self) -> None:
        """
        Select db.
        """
        match self.cfg.file:
            case FileConfig():
                self.db = JSONSaverFile(self.cfg.file_path)

            case _:
                raise TypeError("! Unknown config struct !")
