import json
from dbutils.base import Scoped_session as session
from pathlib import Path

from schemas.interest import InterestSchema

interest_schema = InterestSchema()


def interest_insert():
    with open(
        str(Path().resolve().parent) + "/interests/interest.txt", "r"
    ) as interests:
        interests = list(set([city.strip() for city in interests.readlines()][1::2]))
        interest_dict_list = [
            json.loads("{" + '"name": "{}"'.format(interest) + "}")
            for interest in interests
        ]
        interests = [
            interest_schema.load(interest, session=session)
            for interest in interest_dict_list
        ]

        session.bulk_save_objects(interests)
        session.commit()
        session.remove()


# interest_insert()
