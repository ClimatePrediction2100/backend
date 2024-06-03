from typing import Optional
from pydantic import BaseModel, field_validator


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
    "SSP5-3.4": "534",
    "SSP5-8.5": "585"
}

season_mapping = {
    "연평균": "Yearly",
    "봄": "Spring",
    "여름": "Summer",
    "가을": "Fall",
    "겨울": "Winter"
}

def get_key_from_value(mapping, value):
    return next((k for k, v in mapping.items() if v == value), value)


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

    @field_validator('season')
    def convert_season(cls, value):
        if value in season_mapping:
            return season_mapping[value]
        return value

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
    ssp: str
    season: str
    observeds: list[Observed]
    predicteds: list[Predicted]

    @field_validator('location')
    def reverse_convert_location(cls, value):
        return get_key_from_value(continent_mapping, value)

    @field_validator('ssp')
    def reverse_convert_ssp(cls, value):
        return get_key_from_value(ssp_mapping, value)

    @field_validator('season')
    def reverse_convert_season(cls, value):
        return get_key_from_value(season_mapping, value)
    

if __name__ == "__main__":

    condition = Condition(
        location="아시아",
        ssp="SSP1-1.9",
        season="연평균",
    )

    print(condition)

    result = Result(
        location="Asia",
        ssp="119",
        season=None,
        observeds=[],
        predicteds=[]
    )

    print(result)