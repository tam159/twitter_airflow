from sqlalchemy import Column, String
from dbutils.base import Base


class AlembicApiModel(Base):
    __tablename__ = "alembic_api"

    version_num = Column(String, primary_key=True)
