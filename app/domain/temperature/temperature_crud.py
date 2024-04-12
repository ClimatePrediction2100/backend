from datetime import datetime

from app.domain.temperature.temperature_schema import Condition
from app.models import Observed, Predicted, Location, Coordinate
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, column


async def get_location_id(db: Session, location_name: str):
    stmt = select(Location.id).where(Location.name == location_name)
    location_id = (await db.execute(stmt)).scalar_one()
    return location_id


async def get_coordinate_list(db: Session, location_id: int):
    stmt = select(Coordinate.latitude, Condition.longitude).where(
        Coordinate.location_id == location_id
    )
    coordinate_list = (await db.execute(stmt)).scalars().all()
    return coordinate_list


async def get_observed_list(db: Session, condition: Condition):
    stmt = (
        select(Observed)
        .where(Observed.season == condition.season)
        .where(Observed.latitude == condition.latitude)
        .where(Observed.longitude == condition.longitude)
    )
    observed_list = (await db.execute(stmt)).scalars().all()
    return observed_list


async def get_predicted_list(db: Session, condition: Condition):
    stmt = (
        select(Predicted)
        .where(Predicted.ssp == condition.ssp)
        .where(Predicted.season == condition.season)
        .where(Predicted.latitude == condition.latitude)
        .where(Predicted.longitude == condition.longitude)
    )
    predicted_list = (await db.execute(stmt)).scalars().all()
    return predicted_list


# async def get_temperature_list(db: Session):
#     stmt = select(Temperature)
#     temperature_list = (await db.execute(stmt)).scalars().all()
#     return temperature_list


# async def get_temperature(db: Session, temperature_id: int):
#     stmt = select(Temperature).where(Temperature.id == temperature_id)
#     temperature = (await db.execute(stmt)).scalar_one()
#     return temperature


# async def create_temperature(db: Session, temperature_create: TemperatureCreate):
#     db_temperature = Temperature(
#         condition_id=temperature_create.condition_id,
#         date=temperature_create.date,
#         latitude=temperature_create.latitude,
#         longitude=temperature_create.longitude,
#         highest=temperature_create.highest,
#         average=temperature_create.average,
#         lowest=temperature_create.lowest,
#     )
#     db.add(db_temperature)
#     await db.commit()
