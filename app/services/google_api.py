from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models.charity_project import CharityProject

FORMAT = '%Y/%m/%d %H:%M:%S'

MAX_ROW = 5000
MAX_COLUMN = 2000

FAILED_UPDATE = (
    'Обновляемые данные выходят за допустимый диапазон в таблице'
    f'Доступный объем записи: R1C1:R{MAX_ROW}C{MAX_COLUMN}'
    'Текущий диапазон составляет: R1C1:R{row_count}C{column_count}'
)

TABLE_VALUES = [
    ['Отчет от', '{now_date_time}'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]

SPREADSHEET_BODY = dict(
    properties=dict(
        title='Отчет на {now_date_time}',
        locale='ru_RU'
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист 1',
        gridProperties=dict(
            rowCount=MAX_ROW,
            columnCount=MAX_COLUMN
        )
    ))]
)


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body=None
) -> tuple[str, str]:
    spreadsheet_body = (
        spreadsheet_body if spreadsheet_body else deepcopy(SPREADSHEET_BODY)
    )
    spreadsheet_body['properties']['title'] = (
        spreadsheet_body['properties']['title'].format(
            now_date_time=datetime.now().strftime(FORMAT)
        )
    )
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(
            json=spreadsheet_body
        )
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permission(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json={
                'type': 'user',
                'role': 'writer',
                'emailAddress': settings.email
            },
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    table_values = deepcopy(TABLE_VALUES)
    table_values[0][1] = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values.extend([
        [project.name,
         project.close_date.strftime(FORMAT),
         project.description] for project in charity_projects
    ])
    row_count, column_count = len(table_values), max(map(len, table_values))
    if row_count > MAX_ROW or column_count > MAX_COLUMN:
        raise ValueError(
            FAILED_UPDATE.format(
                row_count=row_count,
                column_count=column_count
            )
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'Лист 1!R1C1:R{row_count}C{column_count}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    )
