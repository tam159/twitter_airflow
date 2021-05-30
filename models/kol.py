from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    DateTime,
    BOOLEAN,
    ForeignKey,
    func,
)
from datetime import datetime
from dbutils.base import Base
from typing import List
from dbutils.base import session_scope


class KolModel(Base):
    __tablename__ = "kols"

    screen_name = Column(String, primary_key=True)
    id = Column(BigInteger, ForeignKey("users.id"), unique=True)
    full_name = Column(String)
    email = Column(String)
    phone = Column(BigInteger)
    priority = Column(Integer)
    crawled_profile = Column(BOOLEAN)
    error_code = Column(Integer)
    error = Column(String)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )
    fans_ids_count = Column(Integer)
    fans_ids_last_crawled = Column(DateTime)
    fans_profiles_count = Column(Integer)
    fans_profiles_last_crawled = Column(DateTime)

    def __repr__(self):
        return "<Kol(screen_name={self.screen_name!r}, id={self.id})>".format(self=self)

    @classmethod
    def find_all(cls) -> List["KolModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> "KolModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        with session_scope() as session:
            session.add(self)

    def delete_from_db(self) -> None:
        with session_scope() as session:
            session.delete(self)
