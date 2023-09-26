from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[int] = Field(None, ge=1)

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100)
    description: str = Field(...)
    full_amount: int = Field(..., ge=1)


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDb(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
