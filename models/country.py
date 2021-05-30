from sqlalchemy import Column, String, DateTime, func
from datetime import datetime
from dbutils.base import Base
from typing import List
from sqlalchemy.orm import relationship
from dbutils.base import session_scope


class CountryModel(Base):
    __tablename__ = "countries"

    country_code = Column(String, primary_key=True)
    country_name = Column(String, nullable=False, unique=True)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    cities = relationship("CityModel", backref="country", lazy="dynamic")
    users = relationship("UserModel", backref="country", lazy="dynamic")

    def __repr__(self):
        return "<Country(country_code={self.country_code!r}, country_name={self.country_name!r})>".format(
            self=self
        )

    @classmethod
    def find_all(cls) -> List["CountryModel"]:
        return cls.query.all()

    @classmethod
    def find_by_country_name(cls, country_name: str) -> "CountryModel":
        return cls.query.filter_by(country_name=country_name).first()

    def save_to_db(self) -> None:
        with session_scope() as session:
            session.add(self)

    def delete_from_db(self) -> None:
        with session_scope() as session:
            session.delete(self)
