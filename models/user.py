from sqlalchemy import (
    Column,
    ForeignKey,
    BigInteger,
    BOOLEAN,
    SmallInteger,
    String,
    DateTime,
    Text,
    func,
    Table,
)
from datetime import datetime
from dbutils.base import Base
from typing import List
from sqlalchemy.orm import relationship, backref
from dbutils.base import session_scope
from dbutils.base import Scoped_session as session

fans = Table(
    "fans",
    Base.metadata,
    Column("followed_id", BigInteger, ForeignKey("users.id"), primary_key=True),
    Column("follower_id", BigInteger, ForeignKey("users.id"), primary_key=True),
)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    id_str = Column(String)
    screen_name = Column(String, unique=True)
    name = Column(String)
    description = Column(Text)
    created_at = Column(DateTime)
    profile_background_image_url = Column(Text)
    profile_background_image_url_https = Column(Text)
    profile_banner_url = Column(Text)
    profile_image_url = Column(Text)
    profile_image_url_https = Column(Text)
    profile_background_tile = Column(BOOLEAN)
    profile_use_background_image = Column(BOOLEAN)
    default_profile = Column(BOOLEAN)
    default_profile_image = Column(BOOLEAN)
    protected = Column(BOOLEAN, index=True)
    following = Column(BOOLEAN)
    verified = Column(BOOLEAN)
    contributors_enabled = Column(BOOLEAN)
    geo_enabled = Column(BOOLEAN)
    has_extended_profile = Column(BOOLEAN)
    is_translation_enabled = Column(BOOLEAN)
    is_translator = Column(BOOLEAN)
    translator_type = Column(String)
    location = Column(String)
    country_code = Column(String, ForeignKey("countries.country_code"))
    city_code = Column(String, ForeignKey("cities.city_code"), index=True)
    birthyear = Column(SmallInteger)
    age = Column(SmallInteger, index=True)
    gender = Column(String, index=True)
    ag_ai_version = Column(String)
    url = Column(String)
    entities_display_url = Column(String)
    entities_expanded_url = Column(Text)
    entities_url = Column(String)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    followers = relationship(
        "UserModel",
        secondary=fans,
        primaryjoin=(fans.c.followed_id == id),
        secondaryjoin=(fans.c.follower_id == id),
        backref=backref("friends", lazy="dynamic"),
        lazy="dynamic",
    )

    interests = relationship("UserInterestModel", backref="users", lazy="dynamic")
    user_stats = relationship("UserStatModel", backref="user", lazy="dynamic")
    kol = relationship("KolModel", backref="user", uselist=False)
    fan_demo_ages = relationship("FanDemoAgeModel", backref="user", lazy="dynamic")
    fan_demo_genders = relationship(
        "FanDemoGenderModel", backref="user", lazy="dynamic"
    )
    fan_demo_cities = relationship("FanDemoCityModel", backref="user", lazy="dynamic")
    fan_demo_countries = relationship(
        "FanDemoCountryModel", backref="user", lazy="dynamic"
    )
    fan_demo_interests = relationship(
        "FanDemoInterestModel", backref="user", lazy="dynamic"
    )

    def __repr__(self):
        return "<User(id={self.id}, screen_name={self.screen_name!r})>".format(
            self=self
        )

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    @classmethod
    def find_by_screen_name(cls, screen_name: str) -> "UserModel":
        return cls.query.filter_by(screen_name=screen_name).first()

    def save_to_db(self) -> None:
        with session_scope() as session:
            session.add(self)

    def delete_from_db(self) -> None:
        with session_scope() as session:
            session.delete(self)

    def is_following(self, user):
        return (
            session.query(fans)
            .filter(fans.c.follower_id == self.id, fans.c.followed_id == user.id)
            .first()
        )
        # return self.friends.filter(fans.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            user_tup = (
                session.query(UserModel.id).filter(UserModel.id == user.id).first()
            )
            if user_tup:
                session.execute(
                    fans.insert(), {"followed_id": user_tup.id, "follower_id": self.id}
                )
            else:
                self.friends.append(user)
            session.commit()
            return False
        else:
            return True

    def unfollow(self, user):
        if self.is_following(user):
            self.friends.remove(user)

    def has_follower(self, user):
        return (
            session.query(fans)
            .filter(fans.c.followed_id == self.id, fans.c.follower_id == user.id)
            .first()
        )
        # return self.followers.filter(fans.c.follower_id == user.id).count() > 0

    def add_follower(self, user):
        if not self.has_follower(user):
            user_tup = (
                session.query(UserModel.id).filter(UserModel.id == user.id).first()
            )
            if user_tup:
                session.execute(
                    fans.insert(), {"followed_id": self.id, "follower_id": user_tup.id}
                )
            else:
                self.followers.append(user)
            session.commit()
            return False
        else:
            return True

    def remove_follower(self, user):
        if self.has_follower(user):
            self.followers.remove(user)
