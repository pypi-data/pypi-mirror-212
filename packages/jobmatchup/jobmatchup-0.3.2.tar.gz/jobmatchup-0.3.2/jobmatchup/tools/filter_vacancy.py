from functools import singledispatch


__all__ = ["filter_vacancies"]


@singledispatch
def filter_vacancies(vacancies, filter_words):
    """
    Filtering Vacancies objects.
    :param vacancies: Vacancies objects
    :param filter_words: list of words to filter
    :return:
    """
    raise TypeError(f"! Value type > {vacancies.__class__} < is not correct !")


@filter_vacancies.register
def _(vacancies: dict, filter_words: list):
    """
    Filtering Vacancies objects.
    :param vacancies: dict with Vacancies objects
    """
    return {
        k: [
            vacancy
            for vacancy in vacancies
            if any([w in vacancy.requirements for w in filter_words])
        ]
        for k, v in vacancies.items()
    }


@filter_vacancies.register
def _(vacancies: list, filter_words: list):
    """
    Filtering Vacancies objects.
    :param vacancies: list with Vacancies objects
    """
    return [
        vacancy
        for vacancy in vacancies
        if any([w in vacancy.requirements for w in filter_words])
    ]
