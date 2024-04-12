import datetime

from typing import Optional
from pydantic import BaseModel, field_validator


class Condition(BaseModel):
    location: Optional[str] = None
    latitude: Optional[int] = None
    longitude: Optional[int] = None
    ssp: int
    season: int


class Observed(BaseModel):
    class Config:
        from_attributes = True

    year: int
    average: float


class Predicted(BaseModel):
    class Config:
        from_attributes = True

    year: int
    highest: float
    average: float
    lowest: float


class Result(BaseModel):
    class Config:
        from_attributes = True

    observeds: list[Observed]
    predicteds: list[Predicted]


class Temperature(BaseModel):
    id: int
    condition_id: int
    date: datetime.date
    latitude: int
    longitude: int
    highest: float
    average: float
    lowest: float


class TemperatureCreate(BaseModel):
    condition_id: int
    date: datetime.date
    latitude: int
    longitude: int
    highest: float
    average: float
    lowest: float

    @field_validator(
        "condition_id", "date", "latitude", "longitude", "highest", "average", "lowest"
    )
    def not_empty(cls, v):
        if v == None:
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v
