from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, DateTime, func
from datetime import datetime
from dbutils.base import Base
from typing import List
from sqlalchemy.orm import relationship
from dbutils.base import session_scope


class FanDemoCityModel(Base):
    __tablename__ = "fan_demo_cities"

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    city_code = Column(String, ForeignKey("cities.city_code"), primary_key=True)
    count = Column(Integer, nullable=False)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    def __repr__(self):
        return "<FanDemoCity(user_id={self.user_id}, city_code={self.city_code!r}, count={self.count})>".format(
            self=self
        )
