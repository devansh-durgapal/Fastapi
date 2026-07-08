from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with sessionLocal() as session:
        yield session


class Base(DeclarativeBase):
    pass
