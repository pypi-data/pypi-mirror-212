from functools import singledispatch


__all__ = ["sort_vacancies_by_salary"]


@singledispatch
def sort_vacancies_by_salary(vacancies):
    """
    Sorting vacancies.
    :param vacancies: Vacancy object
    """
    raise TypeError(f"! Value type > {vacancies.__class__} < is not correct !")


@sort_vacancies_by_salary.register
def _(vacancies: dict):
    """
    Sorting vacancies.
    :param vacancies: dict with Vacancies obj
    :return: sorted dict
    """
    return {
        k: sorted(v, key=lambda x: (x.salary_min, x.salary_max))
        for k, v in vacancies.items()
    }


@sort_vacancies_by_salary.register
def _(vacancies: list):
    """
    Sorting vacancies.
    :param vacancies: list with Vacancies obj
    :return: sorted list
    """
    return sorted(vacancies, key=lambda x: (x.salary_min, x.salary_max))
