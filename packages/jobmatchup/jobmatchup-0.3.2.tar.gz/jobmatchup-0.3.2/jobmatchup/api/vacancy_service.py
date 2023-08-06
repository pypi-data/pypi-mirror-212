from typing import runtime_checkable, Protocol

from ..entity import VacancyDefault


__all__ = ["VacancyServiceInterface"]


@runtime_checkable
class VacancyServiceInterface(Protocol):
    """
    API interface.
    """

    def get_vacancies(self, search: str, amt: int | str) -> list[VacancyDefault, ...]:
        ...
