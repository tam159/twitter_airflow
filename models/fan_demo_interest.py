from sqlalchemy import Column, ForeignKey, BigInteger, Integer, DateTime, func
from datetime import datetime
from dbutils.base import Base
from typing import List
from dbutils.base import session_scope


class FanDemoInterestModel(Base):
    __tablename__ = "fan_demo_interests"

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    interest_id = Column(Integer, ForeignKey("interests.id"), primary_key=True)
    count = Column(Integer, nullable=False)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    def __repr__(self):
        return "<FanDemoInterest(user_id={self.user_id}, interest_id={self.interest_id}, count={self.count})>".format(
            self=self
        )
