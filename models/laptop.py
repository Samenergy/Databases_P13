from pydantic import BaseModel
from typing import Optional

class Laptop(BaseModel):
    brand: str
    processor: str
    ram_gb: int
    storage: str
    gpu: str
    screen_size_inch: float
    resolution: str
    battery_life_hours: float
    weight_kg: float
    operating_system: str
    price_usd: float
    
    class Config:
        # MongoDB database and collection names
        arbitrary_types_allowed = True
