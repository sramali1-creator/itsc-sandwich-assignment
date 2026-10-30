from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ResourceBase(BaseModel):
    item: str = Field(..., min_length=1, max_length=100)
    amount: int = Field(..., ge=0)


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    item: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[int] = Field(None, ge=0)


class Resource(ResourceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
