import datetime

from pydantic import BaseModel, field_validator


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
