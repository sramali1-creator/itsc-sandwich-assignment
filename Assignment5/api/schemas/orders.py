from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .order_details import OrderDetail


class OrderBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=300)


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=300)


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: List[OrderDetail] = []

    model_config = ConfigDict(from_attributes=True)
