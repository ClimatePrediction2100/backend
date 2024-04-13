from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, exists, delete
from starlette import status

from app.database import get_db

from app.domain.temperature import temperature_crud, temperature_schema

from app.models import Observed, Predicted, Location

import random

router = APIRouter(
    prefix="/temperature",
)


@router.get("", response_model=temperature_schema.Result)
async def get_result_list(
    db: Session = Depends(get_db), condition: temperature_schema.Condition = Depends()
):
    if condition.location is not None:
        location = await temperature_crud.get_location(db, condition.location)
        if location is None:
            return []
        else:
            condition.latitude = location.latitude
            condition.longitude = location.longitude
    observeds = await temperature_crud.get_observed_list(db, condition)
    predicteds = await temperature_crud.get_predicted_list(db, condition)
    result = temperature_schema.Result(latitude=condition.latitude, longitude=condition.longitude, observeds=observeds, predicteds=predicteds)
    return result


@router.get("/location", response_model=list[temperature_schema.Location])
async def get_location_list(db: Session = Depends(get_db)):
    locations = await temperature_crud.get_location_list(db)
    return locations


@router.post("/location", status_code=status.HTTP_201_CREATED)
async def create_location(db: Session = Depends(get_db), location: temperature_schema.Location = Depends()):
    db.add(Location(
        name=location.name,
        latitude=location.latitude,
        longitude=location.longitude
    ))
    await db.commit()

@router.delete("/location", status_code=status.HTTP_200_OK)
async def delete_location(db: Session = Depends(get_db), location_name: temperature_schema.LocationName = Depends()):
    stmt = delete(Location).where(Location.name == location_name.name)
    await db.execute(stmt)
    await db.commit()


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

                        interval = dummy.interval * (year - 2014) / (2100 - 2014)

                        lowest = average - random.uniform(interval, interval * dummy.degree)
                        highest = average + random.uniform(interval, interval * dummy.degree)

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
