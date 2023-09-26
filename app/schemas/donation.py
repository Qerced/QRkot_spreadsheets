from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreateDonation(BaseModel):
    full_amount: int = Field(..., ge=1)
    comment: Optional[str]


class UserDonationDb(CreateDonation):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class AllDonationDb(UserDonationDb):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
