from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import AllDonationDb, CreateDonation, UserDonationDb
from app.services.transaction import investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[AllDonationDb],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donation(session: AsyncSession = Depends(get_async_session)):
    """Только для суперюзеров.
    Получает список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=UserDonationDb,
    response_model_exclude_none=True
)
async def create_donation(
    donation: CreateDonation,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Сделать пожертвование."""
    user_donation = await donation_crud.create(
        donation, session, commit_changes=False, user=user
    )
    session.add_all(
        (*investment(
            user_donation,
            await charity_crud.get_not_fully_invested(session)
        ), user_donation)
    )
    await session.commit()
    await session.refresh(user_donation)
    return user_donation


@router.get('/my', response_model=list[UserDonationDb])
async def get_user_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Получить список моих пожертвований."""
    return await donation_crud.get_donations_from_user(user.id, session)
