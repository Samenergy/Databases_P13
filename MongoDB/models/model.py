from pydantic import BaseModel
from typing import Optional

class Laptop(BaseModel):
    Brand: str
    Processor: str
    RAM_GB: int
    Storage: str
    GPU: str
    Screen_Size_inch: float
    Resolution: str
    Battery_Life_Hours: float
    Weight_Kg: float
    Operating_System: str
    Price_Dollars: Optional[float] = None  

class LaptopInResponse(Laptop):
    _id: str  # MongoDB ObjectId as string
