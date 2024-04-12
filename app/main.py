from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from app.domain.temperature import temperature_router

app = FastAPI()

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(temperature_router.router)
