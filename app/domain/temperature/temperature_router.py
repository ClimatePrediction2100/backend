from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from starlette import status

from app.database import get_db

from app.domain.temperature import temperature_crud, temperature_schema

router = APIRouter(
    prefix="/api/temperature",
)


@router.get("/list", response_model=list[temperature_schema.Temperature])
async def get_temperature_list(db: Session = Depends(get_db)):
    temperature_list = await temperature_crud.get_temperature_list(db)
    return temperature_list


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
async def create_temperature(
    temperature_create: temperature_schema.TemperatureCreate,
    db: Session = Depends(get_db),
):
    await temperature_crud.create_temperature(db, temperature_create)
