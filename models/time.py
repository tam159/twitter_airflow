from sqlalchemy import Column, String, Integer, SmallInteger, Time
from dbutils.base import Base
from sqlalchemy.orm import relationship


class TimeModel(Base):
    __tablename__ = "times"

    id = Column(Integer, primary_key=True, autoincrement=False)
    time = Column(Time, nullable=False, unique=True)
    hour = Column(SmallInteger, nullable=False)
    hourap = Column(SmallInteger, nullable=False)
    minute = Column(Integer, nullable=False)
    second = Column(Integer, nullable=False)
    minute_of_day = Column(Integer, nullable=False)
    second_of_day = Column(Integer, nullable=False)
    quarter_hour = Column(String, nullable=False)
    am_pm = Column(String, nullable=False)
    day_night = Column(String, nullable=False)
    day_night_abbrev = Column(String, nullable=False)
    time_period = Column(String, nullable=False)
    time_period_abbrev = Column(String, nullable=False)

    user_stats = relationship("UserStatModel", backref="times", lazy="dynamic")

    def __repr__(self):
        return
        "<Time(id={self.id}, time={self.time})>".format(self=self)
