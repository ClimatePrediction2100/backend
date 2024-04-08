import datetime

from pydantic import BaseModel, field_validator

from app.domain.temperature.temperature_schema import Temperature


class Condition(BaseModel):
    id: int
    co2: float
    metan: float


class ConditionCreate(BaseModel):
    co2: float
    metan: float


class ConditionWithTemperatures(Condition):
    temperatures: list[Temperature] = []
