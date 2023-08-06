from asyncio import run as asyncio_run
from asyncio import TaskGroup as asyncio_TaskGroup

from ..entity import VacancyDefault
from ..configs import Config
from .hh_api import HeadHunterAPI
from .superjob_api import SuperJobAPI


__all__ = ["Query"]


class Query:
    """
    String search.
    """

    result: dict[str, list[VacancyDefault, ...]] = dict()

    def __init__(
        self, cfg: Config, search: str, amt: int = 0, async_work: bool = False
    ):
        """
        Init class.
        :param cfg: config
        :param search: what are we looking for
        :param amt: how many vacancies from api
        :param async_work: sync or async request
        """
        self.search = search
        self.amt = amt
        self.async_work = async_work
        self._cfg = cfg

    def get_hh(self) -> list[VacancyDefault, ...]:
        """
        Receiving Vacancies objects from hh.ru
        """
        return HeadHunterAPI().get_vacancies(search=self.search, amt=self.amt)

    async def _get_hh_async(self) -> None:
        """
        Receiving Vacancies objects from hh.ru (async).
        """
        self.result["hh"] = HeadHunterAPI().get_vacancies(
            search=self.search, amt=self.amt
        )

    def get_sj(self) -> list[VacancyDefault, ...]:
        """
        Receiving Vacancies objects from superjob.ru
        """
        return SuperJobAPI(
            self._cfg.app_info,
            self._cfg.token_info,
        ).get_vacancies(search=self.search, amt=self.amt)

    async def _get_sj_async(self) -> None:
        """
        Receiving Vacancies objects from superjob.ru (async).
        """
        self.result["s_j"] = SuperJobAPI(
            self._cfg.app_info,
            self._cfg.token_info,
        ).get_vacancies(search=self.search, amt=self.amt)

    def get_all(self) -> dict[str, list[VacancyDefault, ...]]:
        """
        Receiving Vacancies objects from superjob.ru and hh.ru.
        """
        self.check_cfg()

        if self.async_work:
            asyncio_run(self._get_all_async())
            return self.result

        return {
            "hh": self.get_hh(),
            "s_j": self.get_sj(),
        }

    async def _get_all_async(self) -> None:
        # async = + ~60% performance
        async with asyncio_TaskGroup() as tg:
            for item in (self._get_hh_async, self._get_sj_async):
                tg.create_task(item())

    def check_cfg(self):
        """
        Validate attrs.
        """
        if self._cfg.without_auth:
            raise ValueError("! you can only use >> get_hh << method !")
        if not all(
            (
                *self._cfg.token_info.dict().values(),
                *self._cfg.app_info.dict().values(),
            )
        ):
            raise ValueError("! authentication config not found !")
