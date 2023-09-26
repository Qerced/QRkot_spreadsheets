from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_charity_id_by_name(
        self, name: str, session: AsyncSession
    ) -> CharityProject:
        charity_id = await session.execute(
            select(self.model).where(self.model.name == name)
        )
        return charity_id.scalars().first()

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> list[CharityProject]:
        charity_projects = await session.execute(
            select(self.model).where(self.model.fully_invested == 1).order_by(
                self.model.close_date
            )
        )
        return charity_projects.scalars().all()


charity_crud = CRUDCharityProject(CharityProject)
