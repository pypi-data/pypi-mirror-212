from typing import Literal

from pydantic import BaseModel, AnyUrl, Field, NonNegativeInt, PositiveInt


__all__ = ["SuperJobAPIVacancies"]


class FieldsIDTitle(BaseModel):
    id: NonNegativeInt
    title: str


class ObjectsCataloguesPositions(BaseModel):
    id: PositiveInt
    key: PositiveInt
    title: str


class ObjectsCatalogues(BaseModel):
    id: PositiveInt
    key: PositiveInt
    positions: list[ObjectsCataloguesPositions]
    title: str


class ObjectsTown(BaseModel):
    declension: str
    genitive: str
    has_metro: bool = Field(alias="hasMetro")
    id: PositiveInt
    title: str


class ObjectsPhones(BaseModel):
    additional_number: str | None = Field(alias="additionalNumber")
    number: str | None


class ObjectsClient(BaseModel):
    address: str | None
    addresses: list | None
    client_logo: AnyUrl | None
    description: str | None
    id: PositiveInt | None
    industry: list
    is_blocked: bool | None
    link: AnyUrl | None
    registered_date: PositiveInt | None
    short_reg: bool | None
    staff_count: str | None
    title: str | None
    town: ObjectsTown | None
    url: AnyUrl | None
    vacancy_count: int | None


class SuperJobAPIVacanciesObject(BaseModel):
    address: str | None
    age_from: NonNegativeInt
    age_to: NonNegativeInt
    agency: FieldsIDTitle
    agreement: bool
    already_sent_on_vacancy: bool
    anonymous: bool
    can_edit: bool = Field(alias="canEdit")
    candidat: str
    catalogues: list[ObjectsCatalogues]
    children: FieldsIDTitle
    client: ObjectsClient
    client_logo: AnyUrl | None
    compensation: None
    contact: str | None
    covid_vaccination_requirement: FieldsIDTitle
    currency: Literal["rub", "uah", "uzs"]
    date_archived: NonNegativeInt
    date_pub_to: PositiveInt
    date_published: PositiveInt
    driving_licence: list
    education: FieldsIDTitle
    experience: FieldsIDTitle
    external_url: AnyUrl | None
    favorite: bool
    fax: None
    faxes: None
    firm_activity: str | None
    firm_name: str
    gender: FieldsIDTitle
    highlight: bool
    id: PositiveInt
    id_client: NonNegativeInt
    is_blacklisted: bool = Field(alias="isBlacklisted")
    is_archive: bool
    is_closed: bool
    is_storage: bool
    languages: list
    latitude: float | None
    link: AnyUrl
    longitude: float | None
    marital_status: FieldsIDTitle = Field(alias="maritalstatus")
    metro: list
    moveable: bool
    salary_minimal: NonNegativeInt = Field(alias="payment_from")
    salary_maximum: NonNegativeInt = Field(alias="payment_to")
    phone: str | None
    phones: list[ObjectsPhones] | None
    place_of_work: FieldsIDTitle
    profession: str
    rejected: bool
    response_info: list
    town: ObjectsTown
    type_of_work: FieldsIDTitle
    vacancy_rich_text: str = Field(alias="vacancyRichText")
    work: None


class SuperJobAPIVacancies(BaseModel):
    more: bool
    objects: list[SuperJobAPIVacanciesObject]
    subscription_active: bool
    subscription_id: NonNegativeInt
    total: NonNegativeInt
