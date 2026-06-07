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

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
        extra="ignore"
    )

    db: DBSettings

settings = Settings()