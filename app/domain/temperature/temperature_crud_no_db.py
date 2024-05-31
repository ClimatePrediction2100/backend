from datetime import datetime

from app.domain.temperature.temperature_schema import Condition
from app.models import Observed, Predicted, Location
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, column
import httpx


async def get_temperature_list(location: str, latitude: int, longitude: int, ssp: str, season: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://database:8001/data",
            params={
                "continent": location,
                "latitude": latitude,
                "longitude": longitude,
                "ssp": ssp,
                "season": season,
            }
        )
    response.raise_for_status()
    data = response.json()
    return data