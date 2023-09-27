import copy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models.charity_project import CharityProject

FORMAT = '%Y/%m/%d %H:%M:%S'

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
            rowCount=len(TABLE_VALUES),
            columnCount=len(max(TABLE_VALUES, key=len))
        )
    ))]
)


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body=copy.deepcopy(SPREADSHEET_BODY)
) -> tuple[str, str]:
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
        wrapper_services: Aiogoogle,
        table_values=copy.deepcopy(TABLE_VALUES)
) -> None:
    table_values[0][1] = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values.extend([
        [project.name,
         project.close_date.strftime(FORMAT),
         project.description] for project in charity_projects
    ])
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='Лист 1!R1C1:R{r2}C{c2}'.format(
                r2=len(table_values),
                c2=len(max(table_values, key=len))),
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    )
