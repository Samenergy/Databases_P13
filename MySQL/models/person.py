from sqlalchemy import Column, Integer, String, Float
from config.database import Base

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    education = Column(String(50), nullable=False)
    income = Column(Float, nullable=False)
    emp_exp = Column(Integer, nullable=False)
    home_ownership = Column(String(20), nullable=False)
