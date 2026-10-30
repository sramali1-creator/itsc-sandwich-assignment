from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .sandwiches import Sandwich


class OrderDetailBase(BaseModel):
    amount: int = Field(..., gt=0)


class OrderDetailCreate(OrderDetailBase):
    order_id: int
    sandwich_id: int


class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    sandwich_id: Optional[int] = None
    amount: Optional[int] = Field(None, gt=0)


class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    sandwich_id: int
    sandwich: Optional[Sandwich] = None

    model_config = ConfigDict(from_attributes=True)
