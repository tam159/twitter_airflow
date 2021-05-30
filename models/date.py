from sqlalchemy import Column, String, Integer, Float, Date, Boolean
from dbutils.base import Base
from sqlalchemy.orm import relationship


class DateModel(Base):
    __tablename__ = "dates"

    id = Column(Integer, primary_key=True, autoincrement=False)
    date = Column(Date, nullable=False, unique=True)
    epoch = Column(Float, nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    quarter_month_day = Column(Integer, nullable=False)
    month_day = Column(Integer, nullable=False)
    month_name = Column(String, nullable=False)
    month_abbrev = Column(String, nullable=False)
    weekday_name = Column(String, nullable=False)
    weekday_abbrev = Column(String, nullable=False)
    week_in_month = Column(Integer, nullable=False)
    week_in_year = Column(Integer, nullable=False)
    day_in_week = Column(Integer, nullable=False)
    day_in_year = Column(Integer, nullable=False)
    is_working_day = Column(Boolean, nullable=False)
    year_in_dimension = Column(Integer, nullable=False)
    month_in_dimension = Column(Integer, nullable=False)
    day_in_dimension = Column(Integer, nullable=False)
    iso_year = Column(Integer, nullable=False)
    iso_week_in_year = Column(Integer, nullable=False)
    iso_day_in_year = Column(Integer, nullable=False)
    iso_day_in_week = Column(Integer, nullable=False)

    user_stats = relationship("UserStatModel", backref="dates", lazy="dynamic")

    def __repr__(self):
        return
        "<Date(id={self.id}, date={self.date})>".format(self=self)
