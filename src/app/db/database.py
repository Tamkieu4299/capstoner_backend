from fastapi import Depends
from ..log import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.pool import NullPool
from starlette_context import context
from ..utils.singleton import Singleton
from app.constants.config import Settings

settings = Settings()


@Singleton
class PSQLManager(object):
    def __init__(self) -> None:

        self._Session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False),
            # scopefunc=lambda: context["request_id"],
        )
        # Database URL
        url = f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"

        self._base_engine = create_engine(url=url, echo=True, poolclass=NullPool)


    def get_session(self):
        return self._Session(bind=self._base_engine)

    def get_base_engin(self):
        return self._base_engine

    def remove(self):
        self._Session.remove()

def get_db(manager=Depends(PSQLManager.Instance)):

    session: Session = manager.get_session()

    try:
        yield session
    except SQLAlchemyError as e:
        logger.fatal("An error occurred during a SqlAlchemy operation", exc_info=e)
        if session.in_transaction():
            session.rollback()
    finally:
        manager.remove()

