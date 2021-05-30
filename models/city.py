from sqlalchemy import Column, String, ForeignKey, DateTime, func
from datetime import datetime
from dbutils.base import Base
from typing import List
from sqlalchemy.orm import relationship
from dbutils.base import session_scope


class CityModel(Base):
    __tablename__ = "cities"

    city_code = Column(String, primary_key=True)
    city_name = Column(String, nullable=False)
    country_code = Column(String, ForeignKey("countries.country_code"), nullable=False)
    country_name = Column(String, nullable=False)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    users = relationship("UserModel", backref="city", lazy="dynamic")

    def __repr__(self):
        return (
            "<City(country_code={self.country_code!r}, country_name={self.country_name!r},"
            "city_code={self.city_code!r}, city_name={self.city_name!r})>".format(
                self=self
            )
        )

    @classmethod
    def find_all(cls) -> List["CityModel"]:
        return cls.query.all()

    @classmethod
    def find_by_city_name(cls, city_name: str) -> "CityModel":
        return cls.query.filter_by(city_name=city_name).first()

    def save_to_db(self) -> None:
        with session_scope() as session:
            session.add(self)

    def delete_from_db(self) -> None:
        with session_scope() as session:
            session.delete(self)
