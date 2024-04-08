from datetime import datetime

from app.domain.condition.condition_schema import ConditionCreate
from app.models import Condition, Temperature
from sqlalchemy.orm import Session
from sqlalchemy import select, insert


async def get_condition_list(db: Session):
    stmt = select(Condition)
    condition_list = (await db.execute(stmt)).scalars().all()
    return condition_list


async def get_condition(db: Session, condition_id: int):
    stmt = select(Condition).where(Condition.id == condition_id)
    condition = (await db.execute(stmt)).scalar_one()
    return condition


async def get_condition_with_temperatures(db: Session, condition_id: int):
    stmt = select(Condition).where(Condition.id == condition_id)
    condition = (await db.execute(stmt)).scalar_one()
    stmt = select(Temperature).where(Temperature.condition_id == condition_id)
    temperatures = (await db.execute(stmt)).scalars().all()
    condition.temperatures = temperatures
    return condition


async def create_condition(db: Session, condition_create: ConditionCreate):
    db_condition = Condition(co2=condition_create.co2, metan=condition_create.metan)
    db.add(db_condition)
    await db.commit()
