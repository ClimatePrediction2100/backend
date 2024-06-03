from typing import Optional
from pydantic import BaseModel, field_validator
import re


continent_mapping = {
    "전 세계": "World",
    "아시아": "Asia",
    "유럽": "Europe",
    "아프리카": "Africa",
    "북아메리카": "North America",
    "남아메리카": "South America",
    "오세아니아": "Oceania",
    "남극": "Antarctica"
}


ssp_mapping = {
    "SSP1-1.9": "119",
    "SSP1-2.6": "126",
    "SSP2-4.5": "245",
    "SSP3-7.0": "370",
    "SSP4-3.4": "434",
    "SSP4-6.0": "460",
    "SSP5-3.5": "535",
    "SSP5-8.5": "585"
}


class Condition(BaseModel):
    location: Optional[str] = None
    latitude: Optional[int] = None
    longitude: Optional[int] = None
    ssp: str
    season: str

    @field_validator('location')
    def convert_location(cls, value):
        if value in continent_mapping:
            return continent_mapping[value]
        return value

    @field_validator('ssp')
    def convert_ssp(cls, value):
        if value in ssp_mapping:
            return ssp_mapping[value]
        return value

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

    location: Optional[str]
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