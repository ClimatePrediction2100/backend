from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from app.domain.temperature import temperature_router_no_db

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(temperature_router_no_db.router)
