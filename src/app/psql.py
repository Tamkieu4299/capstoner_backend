from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

Base = declarative_base()


class PSQLFactory:
    def __init__(self, url):
        self.url = url

    def create_sessionmaker(self, **kwds) -> sessionmaker:
        engine = create_engine(
            self.url,
            echo=True,
            poolclass=NullPool,
        )
        return sessionmaker(autocommit=False, autoflush=False, bind=engine)


if __name__ == "__main__":
    factory = PSQLFactory()
    with factory.create_session("INFORMATION_SCHEMA") as session:
        [print(_) for _ in session.execute("select 1")]
