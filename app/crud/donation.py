from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    async def get_donations_from_user(
        self, user_id: int, session: AsyncSession
    ) -> list[Donation]:
        user_donations = await session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return user_donations.scalars().all()


donation_crud = CRUDDonation(Donation)
