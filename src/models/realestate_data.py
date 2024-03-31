from sqlalchemy import  Column, Integer, String, Text, TIMESTAMP, ForeignKey, Enum, Float, Double
from src.config.database import base
from sqlalchemy.sql import func

class RealEstate(base):
    __tablename__ = 'real_estate'

    Id = Column(Integer, primary_key=True)
    Status = Column(Text)
    Bed = Column(Double)
    Bath = Column(Double)
    AcreLot = Column(Double)
    City = Column(Text)
    State = Column(Text)
    ZipCode = Column(Double)
    HouseSize = Column(Double)
    Price = Column(Double)
