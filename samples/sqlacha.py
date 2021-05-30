from sqlalchemy import Column, ForeignKey, BigInteger, Integer, DateTime, func, distinct
from dbutils.base import Scoped_session as session
from pprint import pprint
from models import *
from twitter.tweepy_api import api

# navetive sql query
# result = session.execute(
#     "SELECT * FROM country WHERE country_code=:param", {"param": "vn"}
# )
# print(type(result))
# print(result)
# for r in result:
#     print(type(r))
#     print(r)
#     print(r[2])
#     print(type(r[2]))
# print(result.country_code)

# get by primary key
# print(CountryModel.query.get("vn"))
# print(session.query(KolModel).get(215624638))
# print(CityModel.query.get("hanoi"))

# return all
# countries = session.query(CountryModel).all()
# for country in countries:
#     print(country.country_code + ' ' + country.country_name)

# return first
# vn = session.query(CountryModel).filter(CountryModel.country_code == 'vn').first()
# print(vn.country_code + ' ' + vn.country_name)

# select all, left join ~ outer join
# vn = CityModel.query.outerjoin(CountryModel, CityModel.country).filter(CountryModel.country_code == 'vn').all()
# for city in vn:
#     print(city)
#     print(city.__dict__)
#     pprint(city.__dict__)

# select columns, join, where ilike
# vn = (
#     session.query(CountryModel.country_name)
#     .join(CityModel)
#     .filter(CityModel.city_code.ilike("%hanoi%"))
#     .all()
# )
# print(vn)
# pprint(vn[0].__dict__)
# print(vn[0].city)

# Count, group by, order by
# cities = session.query(CityModel.country_code, func.count(distinct(CityModel.city_code))).group_by(CityModel.country_code).order_by(CityModel.country_code).all()
# print(cities)

# Get followers
# user = (
#     session.query(UserModel).filter(UserModel.screen_name == "realDonaldTrump").first()
# )
# print(user)
# followers_ids = api.followers_ids(user.screen_name)
#
# for fan_id in followers_ids:
#     fan_obj = UserModel(id=fan_id)
#     user.add_follower(fan_obj)
#
# session.commit()
# session.remove()

# Test adding user
