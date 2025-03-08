from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Laptop(Base):
    __tablename__ = "laptops"

    id = Column(Integer, primary_key=True, index=True)
    Brand = Column(String(50), nullable=False)
    Processor = Column(String(50), nullable=False)
    RAM_GB = Column(Integer, nullable=False)
    Storage = Column(String(50), nullable=False)
    GPU = Column(String(50), nullable=False)
    Screen_Size_inch = Column(Float, nullable=False)
    Resolution = Column(String(20), nullable=False)
    Battery_Life_Hours = Column(Float, nullable=False)
    Weight_Kg = Column(Float, nullable=False)
    Operating_System = Column(String(50), nullable=False)
    Price_Dollars = Column(Float, nullable=False)
