from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Date

from app.database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    condition_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    latitude = Column(Integer, nullable=False)
    longitude = Column(Integer, nullable=False)
    highest = Column(Float, nullable=False)
    average = Column(Float, nullable=False)
    lowest = Column(Float, nullable=False)


class Condition(Base):
    __tablename__ = "condition"

    id = Column(Integer, primary_key=True)
    co2 = Column(Float, nullable=True)
    metan = Column(Float, nullable=True)
