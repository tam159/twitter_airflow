from sqlalchemy import Column, ForeignKey, BigInteger, Integer, DateTime, func
from datetime import datetime
from dbutils.base import Base
from typing import List
from dbutils.base import session_scope


class FanDemoGenderModel(Base):
    __tablename__ = "fan_demo_genders"

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    males_count = Column(Integer, nullable=False)
    females_count = Column(Integer, nullable=False)
    null_count = Column(Integer)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    def __repr__(self):
        return "<FanDemoGender(user_id={self.user_id}, males_count={self.males_count}, females_count={self.females_count})>".format(
            self=self
        )
