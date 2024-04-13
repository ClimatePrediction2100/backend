from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, exists, delete
from starlette import status

from app.database import get_db

from app.domain.temperature import temperature_crud, temperature_schema

from app.models import Observed, Predicted

import random

router = APIRouter(
    prefix="/temperature",
)


@router.get("", response_model=temperature_schema.Result)
async def get_result_list(
    db: Session = Depends(get_db), condition: temperature_schema.Condition = Depends()
):
    if condition.location is not None:
        location_id = await temperature_crud.get_location_id(db, condition.location)
        coordinate_list = await temperature_crud.get_coordinate_list(db, location_id)
        condition.latitude = coordinate_list[0].latitude
        condition.longitude = coordinate_list[0].longitude
    observeds = await temperature_crud.get_observed_list(db, condition)
    predicteds = await temperature_crud.get_predicted_list(db, condition)
    result = temperature_schema.Result(observeds=observeds, predicteds=predicteds)
    return result


@router.post("/dummy", status_code=status.HTTP_201_CREATED)
async def generate_dummy(db: Session = Depends(get_db), dummy: temperature_schema.Dummy = Depends()):
    stmt = select(exists().select_from(Observed))
    exist = (await db.execute(stmt)).scalar()
    if exist:
        stmt = delete(Observed)
        await db.execute(stmt)
        stmt = delete(Predicted)
        await db.execute(stmt)
        await db.commit()
    observed_list = []
    for season in range(5):
        for year in range(1850, 2014):
            for latitude in range(0, 2):
                for longitude in range(0, 2):
                    average = (
                        dummy.min_temp
                        + (year - 1850) * (dummy.max_temp - dummy.min_temp) / (2100 - 1850)
                        + random.uniform(-0.05, 0.05)
                    )
                    observed_list.append(
                        Observed(
                            season=season,
                            year=year,
                            latitude=latitude,
                            longitude=longitude,
                            average=average,
                        )
                    )
    predicted_list = []
    for ssp in range(8):
        for season in range(5):
            for year in range(2014, 2101):
                for latitude in range(0, 2):
                    for longitude in range(0, 2):
                        average = (
                            dummy.min_temp
                            + (year - 1850) * (dummy.max_temp - dummy.min_temp) / (2100 - 1850)
                            + random.uniform(-0.05, 0.05)
                        )
                        lowest = average - random.uniform(dummy.interval, dummy.interval * 2)
                        highest = average + random.uniform(dummy.interval, dummy.interval * 2)

                        predicted_list.append(
                            Predicted(
                                ssp=ssp,
                                season=season,
                                year=year,
                                latitude=latitude,
                                longitude=longitude,
                                average=average,
                                lowest=lowest,
                                highest=highest,
                            )
                        )
    db.add_all(observed_list)
    db.add_all(predicted_list)
    await db.commit()
