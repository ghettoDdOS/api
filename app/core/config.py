from pathlib import Path

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='FASTAPI_',
        case_sensitive=True,
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str = 'postgres'

    DATABASE_HOST: str = 'localhost'
    DATABASE_PORT: int = 5432

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            path=self.POSTGRES_DB,
        )

    BASE_DIR: Path = Path(__file__).parent.parent.parent

    MEDIA_URL: str = '/media'

    @computed_field
    @property
    def MEDIA_ROOT(self) -> Path:
        return self.BASE_DIR / 'media'


settings = _Settings()
