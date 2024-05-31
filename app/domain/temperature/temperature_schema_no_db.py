import datetime

from typing import Optional
from pydantic import BaseModel, field_validator


class Condition(BaseModel):
    location: Optional[str] = None
    latitude: Optional[int] = None
    longitude: Optional[int] = None
    ssp: str
    season: str


class Observed(BaseModel):
    class Config:
        from_attributes = True

    year: int
    average: Optional[float] = None


class Predicted(BaseModel):
    class Config:
        from_attributes = True

    year: int
    highest: Optional[float] = None
    average: Optional[float] = None
    lowest: Optional[float] = None


class Result(BaseModel):
    class Config:
        from_attributes = True

    location: Optional[str] = None
    latitude: Optional[int] = None
    longitude: Optional[int] = None
    observeds: list[Observed]
    predicteds: list[Predicted]