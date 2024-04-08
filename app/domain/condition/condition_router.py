from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from starlette import status

from app.database import get_db

from app.domain.condition import condition_crud, condition_schema

router = APIRouter(
    prefix="/api/condition",
)


@router.get("/list", response_model=list[condition_schema.Condition])
async def get_condition_list(db: Session = Depends(get_db)):
    condition_list = await condition_crud.get_condition_list(db)
    return condition_list


@router.get("/detail", response_model=condition_schema.ConditionWithTemperatures)
async def get_condition(condition_id: int = Query(...), db: Session = Depends(get_db)):
    condition = await condition_crud.get_condition_with_temperatures(db, condition_id)
    return condition


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
async def create_condition(
    condition_create: condition_schema.ConditionCreate, db: Session = Depends(get_db)
):
    await condition_crud.create_condition(db, condition_create)
