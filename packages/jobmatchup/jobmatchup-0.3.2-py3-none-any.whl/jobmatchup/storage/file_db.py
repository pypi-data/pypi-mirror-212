from json import dump, loads, JSONDecodeError
from logging import warning as logging_warn

from ..entity.vacancy import VacancyDefault


__all__ = ["JSONSaverFile"]


class JSONSaverFile:
    """
    Class for store in file (json).
    """

    __slots__ = "file_path"

    def __init__(self, file_path: str):
        self.file_path = file_path

    def _read(self) -> list | None:
        """
        Read file.
        """
        try:
            with open(self.file_path) as f:
                try:
                    return loads(f.read())
                except JSONDecodeError:
                    logging_warn("! EMPTY file !")
        except FileNotFoundError as e:
            logging_warn(e)

    def _dump(self, data):
        """
        Write to file.
        """
        with open(self.file_path, "w") as f:
            dump(data, f)

    @staticmethod
    def _remove_repetitions(data: list) -> list:
        return [dict(s) for s in set(frozenset(d.items()) for d in data)]

    def add_vacancy(self, vacancy: list | dict) -> None:
        """
        Save vacancy in file.
        :param vacancy: Vacancy object
        """
        data = self._read()

        if data:
            match vacancy:
                case list():
                    data += [v.dict(by_alias=True) for v in vacancy]
                case dict():
                    data += [v.dict(by_alias=True) for v in sum(vacancy.values(), [])]

            data = self._remove_repetitions(data)
        else:
            match vacancy:
                case list():
                    data = [v.dict(by_alias=True) for v in vacancy]
                case dict():
                    data = [v.dict(by_alias=True) for v in sum(vacancy.values(), [])]

        self._dump(data)

    def get_vacancies_by_salary(self, salary_min: int) -> list:
        """
        Select vacancies by salary.
        :param salary_min: salary
        :return: vacancies objects
        """
        with open(self.file_path) as f:
            data = loads(f.read())

        return [
            VacancyDefault.parse_obj(vacancy)
            for vacancy in data
            if vacancy.get("salary_min") <= salary_min
        ]

    def delete_vacancy(self, vacancy_url: str) -> None:
        """
        Delete vacancy.
        :param vacancy_url: vacancy url
        """
        with open(self.file_path, "x+") as f:
            data: list = loads(f.read())
            for vacancy in data:
                if vacancy.get("url") == vacancy_url:
                    data.remove(vacancy)
            dump(data, f)
