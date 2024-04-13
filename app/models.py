from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Date

from app.database import Base


class Observed(Base):
    __tablename__ = "observed"

    id = Column(Integer, primary_key=True)
    season = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    latitude = Column(Integer, nullable=False)
    longitude = Column(Integer, nullable=False)
    average = Column(Float, nullable=False)


class Predicted(Base):
    __tablename__ = "predicted"

    id = Column(Integer, primary_key=True)
    ssp = Column(Integer, nullable=False)
    season = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    latitude = Column(Integer, nullable=False)
    longitude = Column(Integer, nullable=False)
    highest = Column(Float, nullable=True)
    average = Column(Float, nullable=False)
    lowest = Column(Float, nullable=False)

class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=32), nullable=False)
    latitude = Column(Integer, nullable=False)
    longitude = Column(Integer, nullable=False)