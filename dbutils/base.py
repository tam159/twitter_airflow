from sqlalchemy.ext.declarative import declarative_base
from dbutils.convention import metadata

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from config import DATABASE_URI
from contextlib import contextmanager

Base = declarative_base(metadata=metadata)

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
Scoped_session = scoped_session(sessionmaker(bind=engine))
Base.query = Scoped_session.query_property()


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_database():
    Base.metadata.create_all(engine)


def drop_database():
    Base.metadata.drop_all(engine)
