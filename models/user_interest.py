from sqlalchemy import Column, ForeignKey, BigInteger, Integer
from dbutils.base import Base
from typing import List
from dbutils.base import session_scope


class UserInterestModel(Base):
    __tablename__ = "users_interests"

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    interest_id = Column(Integer, ForeignKey("interests.id"), primary_key=True)
    value = Column(Integer, nullable=False)

    def __repr__(self):
        return "<UserInterest(user_id={self.user_id}, interest_id={self.interest_id}, value={self.value})>".format(
            self=self
        )

    @classmethod
    def find_all(cls) -> List["UserInterestModel"]:
        return cls.query.all()

    @classmethod
    def find_by_user_id(cls, user_id: int) -> List["UserInterestModel"]:
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_interest_id(cls, interest_id: int) -> List["UserInterestModel"]:
        return cls.query.filter_by(interest_id=interest_id).all()

    def save_to_db(self) -> None:
        with session_scope() as session:
            session.add(self)

    def delete_from_db(self) -> None:
        with session_scope() as session:
            session.delete(self)
