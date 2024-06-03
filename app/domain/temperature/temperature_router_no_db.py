from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, exists, delete
from starlette import status

from app.database import get_db

from app.domain.temperature import temperature_crud_no_db, temperature_schema_no_db

from app.models import Observed, Predicted, Location

import random

router = APIRouter(
    prefix="/temperature",
)


@router.get("", response_model=temperature_schema_no_db.Result)
async def get_result_list(condition: temperature_schema_no_db.Condition = Depends()):
    data = await temperature_crud_no_db.get_temperature_list(
        condition.location, condition.latitude, condition.longitude, condition.ssp, condition.season)
    
    if not condition.location:
        data['min'] = data['avg']
        data['max'] = data['avg']

    observeds = []
    for i in range(min(len(data['avg']), 174)):
        observeds.append({
            'year': 1850 + i,
            'average': data['avg'][i]
        })

    predicteds = []
    for i in range(174, len(data['avg'])):
        predicteds.append({
            'year': 1850 + i,
            'highest': data['max'][i],
            'average': data['avg'][i],
            'lowest': data['min'][i]
        })
    
    
    result = temperature_schema_no_db.Result(
        location=condition.location,
        latitude=condition.latitude,
        longitude=condition.longitude,
        observeds=observeds,
        predicteds=predicteds
    )

    return result