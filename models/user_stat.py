from sqlalchemy import Column, ForeignKey, BigInteger, Integer, DateTime, func
from datetime import datetime
from dbutils.base import Base
from typing import List
from dbutils.base import session_scope


class UserStatModel(Base):
    __tablename__ = "user_stats"

    id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    date_id = Column(Integer, ForeignKey("dates.id"), primary_key=True)
    time_id = Column(Integer, ForeignKey("times.id"), primary_key=True)
    followers_count = Column(Integer, nullable=False)
    friends_count = Column(Integer, nullable=False)
    listed_count = Column(Integer, nullable=False)
    favourites_count = Column(BigInteger, nullable=False)
    statuses_count = Column(Integer, nullable=False)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    def __repr__(self):
        return "<UserStat(id={self.id}, date_id={self.date_id}, time_id={self.time_id})>".format(
            self=self
        )

    @classmethod
    def find_all(cls) -> List["UserStatModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> List["UserStatModel"]:
        return cls.query.filter_by(id=_id).all()

    @classmethod
    def find_by_date_id(cls, date_id: int) -> List["UserStatModel"]:
        return cls.query.filter_by(date_id=date_id).all()

    def save_to_db(self) -> None:
        with session_scope() as session:
            session.add(self)

    def delete_from_db(self) -> None:
        with session_scope() as session:
            session.delete(self)
