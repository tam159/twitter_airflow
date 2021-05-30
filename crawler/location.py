from unidecode import unidecode
from sqlalchemy import literal, func
from models.city import CityModel
from models.country import CountryModel
from dbutils.base import Scoped_session as session


def location_maching(user):
    country_city_dict = {"country_code": None, "city_code": None}

    # Lower case, remove spaces, convert to unicode
    locations = unidecode(user.location.lower().replace(" ", ""))

    if locations != "":
        # Select from cities tables where locations contains city_code
        cities = (
            session.query(CityModel)
            .filter(literal(locations).contains(CityModel.city_code))
            .all()
        )

        # If a list is returned
        if len(cities) > 1:
            # Find a city having maximum city_code length
            city_code_max_length = 0
            for city in cities:
                if len(city.city_code) > city_code_max_length:
                    city_code_max_length = len(city.city_code)
                    matched_city = city

            country_city_dict["country_code"] = matched_city.country_code
            country_city_dict["city_code"] = matched_city.city_code

        # If a city is returned
        elif len(cities) == 1:
            country_city_dict["country_code"] = cities[0].country_code
            country_city_dict["city_code"] = cities[0].city_code

        else:
            # If no city return, find a country
            countries_in = (
                session.query(CountryModel)
                .filter(
                    literal(locations).contains(func.lower(CountryModel.country_name))
                )
                .all()
            )
            countries_contain = (
                session.query(CountryModel)
                .filter(func.lower(CountryModel.country_name).contains(locations))
                .all()
            )
            countries = countries_contain + countries_in

            if countries:
                country_city_dict["country_code"] = countries[0].country_code

        session.remove()

    return country_city_dict


# user = api.get_user(212501751)
# print(location_maching(user))
