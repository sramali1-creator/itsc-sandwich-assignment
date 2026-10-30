from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SandwichBase(BaseModel):
    sandwich_name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., ge=0, lt=100)


class SandwichCreate(SandwichBase):
    pass


class SandwichUpdate(BaseModel):
    sandwich_name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, ge=0, lt=100)


class Sandwich(SandwichBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
