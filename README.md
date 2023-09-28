# Благотворительный фонд поддержки котов

Фонд собирает пожертвования на различные целевые проекты: медицинское обслуживание нуждающихся хвостатых, обустройство кошачьей колонии в подвале, корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Технологический стек

* FastAPI
* FastApiUsers
* Pydantic
* Aiogoogle
* SQLAlchemy
* Alembic
* SQLite
* Uvicorn

## Установка

Чтобы установить проект, выполните следующие команды:

```
git clone https://github.com/Qerced/cat_charity_fund.git
cd cat_charity_fund
pip install -r requirements.txt
```

## Настройка

В проекте уже существуют готовые миграции, которые вы можете применить для работы базы данных:

```
alembic upgrade head
```

При необходимости повторной установки Alembic или инициализации собственных миграций, используйте шаблон `async` и автогенерацию:

```
alembic init --template async
alembic revision --autogenerate -m "Migration name"
```

Для заполнения env, необходимо получить [JSON-файл](https://cloud.google.com/iam/docs/keys-create-delete) с ключом доступа к сервисному аккаунту. Руководствуйтесь следующим примером для корректной работы всего проекта:

```
APP_TITLE=Благотворительный фонд поддержки котиков  # Optional
DATABASE_URL=sqlite+aiosqlite:///./charity.db
SECRET=yoursecret
FIRST_SUPERUSER_EMAIL=user@example.com
FIRST_SUPERUSER_PASSWORD=PASSWORD
TYPE=service_account
PROJECT_ID=PROJECT_ID
PRIVATE_KEY_ID=KEY_ID
PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nPRIVATE_KEY\n-----END PRIVATE KEY-----\n
CLIENT_EMAIL=SERVICE_ACCOUNT_EMAIL
CLIENT_ID=CLIENT_ID
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/SERVICE_ACCOUNT_EMAIL
EMAIL_USER=creator_service@example.com
```

## Запуск

Запуск проекта осуществляется командой:

```
uvicorn app.main:app --reload
```

## Использование

В Фонде может быть открыто несколько целевых проектов. Целевые проекты создаются администраторами сайта. Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования в проекты поступают по принципу First In, First Out. Сразу после создания нового проекта или пожертвования запускается процесс «инвестирования».

## API

Чтобы узнать больше о методах реализованных в проекте перейдите по [адресу](127.0.0.1:8000/docs)
или загрузите [файл](https://github.com/Qerced/QRkot_spreadsheets/blob/main/openapi.json) на сайт[redocly](https://redocly.github.io/redoc/)

## Авторы:
- [Vakauskas Vitas](https://github.com/Qerced)
