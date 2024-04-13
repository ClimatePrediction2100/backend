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

    latitude: int
    longitude: int
    observeds: list[Observed]
    predicteds: list[Predicted]


class Dummy(BaseModel):
    class Config:
        from_attributes = True

    min_temp: float = -3.0
    max_temp: float = 3.0
    interval: float = 1.0
    degree: float = 1.5


class Location(BaseModel):
    class Config:
        from_attributes = True

    name: str
    latitude: int
    longitude: int


class LocationName(BaseModel):
    class Config:
        from_attributes = True

    name: str