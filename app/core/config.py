from typing import Optional

from pydantic import BaseSettings

APP_TITLE_DEFAULT = 'QRKot'
QRKOT_URL_DEFAULT = 'sqlite+aiosqlite:///./charity.db'
SECRET_DEFAULT = 'SECRET'
ENV_FILE = '.env'


class Settings(BaseSettings):
    app_title: str = APP_TITLE_DEFAULT
    database_url: str = QRKOT_URL_DEFAULT
    secret: str = SECRET_DEFAULT
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = ENV_FILE


settings = Settings()
