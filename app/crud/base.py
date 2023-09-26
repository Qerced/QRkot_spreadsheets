from datetime import datetime
from typing import Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation, User
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)
from app.schemas.donation import CreateDonation


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(
        self, id: int, session: AsyncSession
    ) -> Union[CharityProject, Donation]:
        object = await session.execute(
            select(self.model).where(self.model.id == id)
        )
        return object.scalars().first()

    async def get_multi(
        self, session: AsyncSession
    ) -> list[Union[CharityProject, Donation]]:
        objects = await session.execute(select(self.model))
        return objects.scalars().all()

    async def get_not_fully_invested(
        self, session: AsyncSession
    ) -> list[Union[CharityProject, Donation]]:
        objects = await session.execute(
            select(self.model).where(
                self.model.fully_invested == 0
            ).order_by(self.model.create_date)
        )
        return objects.scalars().all()

    async def create(
        self,
        schema: Union[CharityProjectCreate, CreateDonation],
        session: AsyncSession,
        commit_changes: bool = True,
        user: Optional[User] = None
    ) -> Union[CharityProject, Donation]:
        data = schema.dict(exclude_unset=True)
        if user is not None:
            data['user_id'] = user.id
        object = self.model(
            **data, invested_amount=0, create_date=datetime.now()
        )
        session.add(object)
        if commit_changes:
            await session.commit()
            await session.refresh(object)
        return object

    async def update(
        self,
        object: CharityProject,
        schema: CharityProjectUpdate,
        session: AsyncSession
    ) -> CharityProject:
        update_data = schema.dict(exclude_unset=True)
        for field in jsonable_encoder(object):
            if field in update_data:
                setattr(object, field, update_data[field])
        session.add(object)
        await session.commit()
        await session.refresh(object)
        return object

    async def delete(
            self, charity_project: CharityProject, session: AsyncSession
    ) -> CharityProject:
        await session.delete(charity_project)
        await session.commit()
        return charity_project
