import json
from dbutils.base import Scoped_session as session
from pathlib import Path

from schemas.city import CitySchema
from schemas.country import CountrySchema


def country_insert():
    country_dict_list = [
        {"country_code": "vn", "country_name": "Vietnam"},
        {"country_code": "th", "country_name": "Thailand"},
        {"country_code": "id", "country_name": "Indonesia"},
    ]

    country_schema = CountrySchema()
    countries = [
        country_schema.load(country, session=session) for country in country_dict_list
    ]

    session.bulk_save_objects(countries)
    session.commit()
    session.remove()


def city_insert(country_code, country_name):
    with open(
        str(Path().resolve().parent) + "/locations/" + country_code + ".txt", "r"
    ) as locations:
        locations = [city.strip() for city in locations.readlines()]
        city_codes = locations[::2]
        city_names = locations[1::2]

        city_dict_list = [
            json.loads(
                "{"
                + '"country_code": "{}", "country_name": "{}", "city_code": "{}", "city_name": "{}"'.format(
                    country_code, country_name, city_codes[i], city_names[i]
                )
                + "}"
            )
            for i in range(len(city_codes))
        ]

        city_schema = CitySchema()

        cities = [city_schema.load(city, session=session) for city in city_dict_list]

        session.bulk_save_objects(cities)
        session.commit()
        session.remove()


# country_insert()
# city_insert('vn', 'Vietnam')
# city_insert('th', 'Thailand')
# city_insert('id', 'Indonesia')
