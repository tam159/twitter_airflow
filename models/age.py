from sqlalchemy import Column, String, Integer, DateTime, func
from datetime import datetime
from dbutils.base import Base
from typing import List
from sqlalchemy.orm import relationship
from dbutils.base import session_scope


class AgeModel(Base):
    __tablename__ = "ages"

    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False)
    min = Column(Integer, nullable=False)
    max = Column(Integer, nullable=False)
    desc = Column(String)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    def __repr__(self):
        return "<Age(id={self.id}, type={self.type!r}, min={self.min}, max={self.max}, desc={self.desc!r})>".format(
            self=self
        )

    @classmethod
    def find_all(cls) -> List["AgeModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> "AgeModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_type(cls, type: str) -> List["AgeModel"]:
        return cls.query.filter_by(type=type).all()

    def save_to_db(self) -> None:
        with session_scope() as session:
            session.add(self)

    def delete_from_db(self) -> None:
        with session_scope() as session:
            session.delete(self)
