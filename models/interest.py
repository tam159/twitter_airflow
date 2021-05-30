from sqlalchemy import Column, String, Integer, DateTime, func
from datetime import datetime
from dbutils.base import Base
from typing import List
from sqlalchemy.orm import relationship
from dbutils.base import session_scope


class InterestModel(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    desc = Column(String)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    users = relationship("UserInterestModel", backref="interests", lazy="dynamic")

    def __repr__(self):
        return "<Interest(name={self.name!r}, desc={self.desc!r})>".format(self=self)

    @classmethod
    def find_all(cls) -> List["InterestModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> "InterestModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name: str) -> "InterestModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        with session_scope() as session:
            session.add(self)

    def delete_from_db(self) -> None:
        with session_scope() as session:
            session.delete(self)
