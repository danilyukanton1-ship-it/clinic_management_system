from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class DBSettings(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    NAME: str

    @property
    def db_url(self):
        return (
            f"postgresql+psycopg2://"
            f"{self.USER}:{self.PASSWORD}@"
            f"{self.HOST}:{self.PORT}/"
            f"{self.NAME}"
        )

    @property
    def async_db_url(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.USER}:{self.PASSWORD}@"
            f"{self.HOST}:{self.PORT}/"
            f"{self.NAME}"
        )


class JWT(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int


class Redis(BaseSettings):
    HOST: str
    PORT: int


class Celery(BaseSettings):
    BROKER_URL: str
    RESULT_BACKEND: str | None = None


class SMTP(BaseSettings):
    API_KEY: str
    FROM: str


class Minio(BaseSettings):
    ACCESS_KEY: str
    ENDPOINT: str
    PUBLIC_ENDPOINT: str
    SECRET_KEY: str
    BUCKET: str
    SECURE: bool


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_nested_delimiter="__", extra="ignore"
    )

    db: DBSettings
    jwt: JWT
    redis: Redis
    celery: Celery
    smtp: SMTP
    minio: Minio

    SLOT_RETENTION_DAYS: int = 365 * 5


settings = Settings()
