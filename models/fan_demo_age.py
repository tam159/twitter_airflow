from sqlalchemy import Column, BigInteger, Integer, ForeignKey, DateTime, func
from datetime import datetime
from dbutils.base import Base
from typing import List
from sqlalchemy.orm import relationship
from dbutils.base import session_scope


class FanDemoAgeModel(Base):
    __tablename__ = "fan_demo_ages"

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    age_id = Column(Integer, ForeignKey("ages.id"), primary_key=True)
    count = Column(Integer, nullable=False)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    def __repr__(self):
        return "<FanDemoAge(user_id={self.user_id}, age_id={self.age_id}, count={self.count})>".format(
            self=self
        )
