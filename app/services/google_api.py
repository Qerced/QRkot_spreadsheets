from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models.charity_project import CharityProject

FORMAT = '%Y/%m/%d %H:%M:%S'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(
            json={
                'properties': {'title': f'Отчет на {now_date_time}',
                               'locale': 'ru_RU'},
                'sheets': [{'properties': {
                    'sheetType': 'GRID',
                    'sheetId': 0,
                    'title': 'Лист 1',
                    'gridProperties': {'rowCount': 100,
                                       'columnCount': 11}
                }}]
            }
        )
    )
    return response['spreadsheetId']


async def set_user_permission(
        spreadsheetId: int,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetId,
            json={
                'type': 'user',
                'role': 'writer',
                'emailAddress': settings.email
            },
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheetId: str,
        charity_projects: list[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in charity_projects:
        table_values.append(
            [project.name,
             project.close_date.strftime(FORMAT),
             project.description]
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetId,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    )
