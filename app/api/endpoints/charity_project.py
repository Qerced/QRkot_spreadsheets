from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import (
    check_before_update, check_duplicate_name, check_invested_amount
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDb, CharityProjectUpdate
)
from app.services.transaction import investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDb],
    response_model_exclude_none=True
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session)
):
    """Получает список всех проектов."""
    return await charity_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDb,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров.
    Создает благотворительный проект."""
    await check_duplicate_name(project, session)
    created_project = await charity_crud.create(
        project, session, commit_changes=False
    )
    session.add_all(
        (*investment(
            created_project,
            await donation_crud.get_not_fully_invested(session)
        ), created_project)
    )
    await session.commit()
    await session.refresh(created_project)
    return created_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDb,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    project: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров.Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной."""
    return await charity_crud.update(
        await check_before_update(project_id, project, session),
        project, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDb,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров.
    Удаляет проект."""
    return await charity_crud.delete(
        await check_invested_amount(project_id, session), session
    )
