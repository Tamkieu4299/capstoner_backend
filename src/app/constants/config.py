from pydantic import BaseSettings
from functools import lru_cache
from ..psql import PSQLFactory


@lru_cache()
def get_settings():
    return Settings()


class Settings(BaseSettings):
    """Config class read from .env"""

    API_VERSION: str
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str
    AWS_S3_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    IMAGE_BUCKET: str
    DEFAULT_REGION: str
    REDIS_HOST = str
    REDIS_PORT = str
    AZURE_ENDPOINT= str
    AZURE_API_KEY = str
    AZURE_API_VERSION= str
    GPT4_AZURE_ENDPOINT= str
    GPT4_AZURE_API_KEY = str
    GPT4_AZURE_API_VERSION= str
    # REDIS_SSL = getattr(settings, 'REDIS_SSL', False)

    @property
    def psql_factory(self) -> PSQLFactory:
        return PSQLFactory(
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOSTNAME}:{self.DATABASE_PORT}/{self.POSTGRES_DB}"
        )


if __name__ == "__main__":
    settings = get_settings()
    factory = settings.psql_factory
    print(factory.__dict__)
