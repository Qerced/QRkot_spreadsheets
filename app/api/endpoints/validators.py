from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate

ALREADY_EXISTS = 'Проект с таким именем уже существует!'
NOT_FOUND = 'Проект не найден!'
CANNOT_BE_DELETED = 'В проект были внесены средства, не подлежит удалению!'
CANNOT_BE_CLOSED = 'Закрытый проект нельзя редактировать!'
CANNOT_BE_CHANGED = 'Запрещено устанавливать требуемую сумму меньше внесённой'


async def check_duplicate_name(
    schema: CharityProjectUpdate, session: AsyncSession
) -> None:
    if schema.name:
        charity_id = await charity_crud.get_charity_id_by_name(
            schema.name, session
        )
        if charity_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ALREADY_EXISTS
            )


async def check_project_exists(
        id: int, session: AsyncSession
) -> Optional[CharityProject]:
    charity_project = await charity_crud.get(id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NOT_FOUND
        )
    return charity_project


async def check_invested_amount(
        id: int, session: AsyncSession
) -> Optional[CharityProject]:
    charity_project = await charity_crud.get(id, session)
    if charity_project.invested_amount or charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CANNOT_BE_DELETED
        )
    return charity_project


async def check_close_project(project: CharityProject) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CANNOT_BE_CLOSED
        )


async def check_before_update(
    id: int, schema: CharityProjectUpdate, session: AsyncSession
) -> Optional[CharityProject]:
    charity_project = await check_project_exists(id, session)
    await check_close_project(charity_project)
    await check_duplicate_name(schema, session)
    if schema.full_amount:
        if schema.full_amount < charity_project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=CANNOT_BE_CHANGED
            )
    return charity_project
