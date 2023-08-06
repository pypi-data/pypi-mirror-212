from datetime import datetime
from logging import error as logging_error
from re import sub
from urllib import request, error

from ..entity.hh import HeadHunterAPIVacancies
from ..entity.vacancy import VacancyDefault

from dateutil.tz import UTC


__all__ = ["HeadHunterAPI"]


class HeadHunterAPI:
    """
    Class for working with API HeadHunter.
    """

    def get_vacancies(self, search: str, amt: int | str) -> list[VacancyDefault, ...]:
        """
        Search query.
        :param amt: how much to get (no more than 100)
        :param search: what we want to find
        :return: received vacancies containing the word (search param) in Vacancy-object
        """
        data_raw: str = self._load_from_url(
            f"https://api.hh.ru/vacancies?text={search}&per_page={amt}"
        )
        vacancies_items = HeadHunterAPIVacancies.parse_raw(data_raw).items

        return [
            VacancyDefault(
                title=item.name,
                url=item.alternate_url,
                date_published_timestamp=self._date_to_timestamp(item.published_at),
                city="не указан"
                if not item.address or not item.address.city
                else item.address.city,
                requirements=self._requirements_formatter(item),
                salary_min=0
                if not item.salary or not item.salary.salary_minimal
                else item.salary.salary_minimal,
                salary_max=0
                if not item.salary or not item.salary.salary_maximum
                else item.salary.salary_maximum,
                currency="RUB"
                if not item.salary
                else self._currency_mapping(item.salary.currency),
            )
            for item in vacancies_items
        ]

    @staticmethod
    def _load_from_url(url: str) -> str | None:
        """
        Load json (from url).
        :param url: URL to upload data
        :return: loaded data from url
        """
        try:
            with request.urlopen(url) as url:
                return url.read().decode()
        except error as e:
            logging_error(f"error :: {repr(e)} ::")

    @staticmethod
    def _currency_mapping(currency: str) -> str | None:
        """
        Mapping currency names.
        param currency: currency abbreviation
        return: correct name
        """
        currency_map: dict = {
            "RUR": "RUB",
            "BYR": "BYN",
            "UAH": "UAH",
            "USD": "USD",
            "EUR": "EUR",
            "KZT": "KZT",
            "UZS": "UZS",
            "KGS": "KGS",
            "AZN": "AZN",
            "GEL": "GEL",
        }
        return currency_map.get(currency)

    @staticmethod
    def _requirements_formatter(item) -> str:
        """
        Collection of information.
        :param item: API answer (in dict)
        :return: info
        """
        if item.snippet.requirement is None:
            desc = "не указано"
        else:
            desc = sub("<[^<]+?>", "", item.snippet.requirement)  # <- remove html
        return (
            f"Опыт: {item.experience.name}\n"
            f"Тип занятости: {item.employment.name}\n"
            f"Описание: {desc}"
        )

    @staticmethod
    def _date_to_timestamp(date_time: datetime) -> int:
        """
        Parse datetime (UTC) and conversion to timestamp
        :param date_time: string representation of a date
        :return: timestamp
        """
        return int(round(date_time.astimezone(UTC).timestamp()))
