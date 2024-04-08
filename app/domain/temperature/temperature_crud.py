from datetime import datetime

from app.domain.temperature.temperature_schema import TemperatureCreate
from app.models import Temperature, Temperature
from sqlalchemy.orm import Session
from sqlalchemy import select, insert


async def get_temperature_list(db: Session):
    stmt = select(Temperature)
    temperature_list = (await db.execute(stmt)).scalars().all()
    return temperature_list


async def get_temperature(db: Session, temperature_id: int):
    stmt = select(Temperature).where(Temperature.id == temperature_id)
    temperature = (await db.execute(stmt)).scalar_one()
    return temperature


async def create_temperature(db: Session, temperature_create: TemperatureCreate):
    db_temperature = Temperature(
        condition_id=temperature_create.condition_id,
        date=temperature_create.date,
        latitude=temperature_create.latitude,
        longitude=temperature_create.longitude,
        highest=temperature_create.highest,
        average=temperature_create.average,
        lowest=temperature_create.lowest,
    )
    db.add(db_temperature)
    await db.commit()
