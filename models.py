from pydantic import BaseModel, Field
from typing import List


class Item(BaseModel):
    shortDescription: str = Field(..., regex="^[\w\s\-]+$")
    price: str = Field(..., regex="^\d+\.\d{2}$")

class Receipt(BaseModel):
    retailer: str = Field(..., regex="^[\w\s\-&]+$")
    purchaseDate: str
    purchaseTime: str
    items: List[Item]
    total: str = Field(..., regex="^\d+\.\d{2}$")

class Points(BaseModel):
    points: int