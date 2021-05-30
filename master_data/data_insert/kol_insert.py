import csv
from datetime import datetime
from dbutils.base import Scoped_session as session
from pathlib import Path

from schemas.kol import KolSchema

kol_schema = KolSchema()

# Update or insert new Kols from excel file to a kols table
def kol_insert():
    with open(
        str(Path().resolve().parent) + "/kols/IDTwitterTest.csv", "r"
    ) as buzzers:
        # Return a list of kols under dictionary format
        kol_dict_list = [dict(kol) for kol in csv.DictReader(buzzers)]

        for kol in kol_dict_list:
            # Clean kol screen_name
            kol["screen_name"] = (
                kol["screen_name"]
                .rstrip("/")
                .split("/")[-1]
                .lstrip("@")
                .strip(" ")
                .lower()
            )

            # Clean kol email
            kol["email"] = kol["email"] if kol["email"] != "" else None

            # Clean kol phone number
            try:
                kol["phone"] = int(kol["phone"])
            except:
                kol["phone"] = None

        for kol in kol_dict_list:
            if "twitter." not in kol["screen_name"]:
                # Add or update kols
                kol["updated_at"] = str(datetime.utcnow())
                kol_obj = kol_schema.load(kol, session=session)
                session.add(kol_obj)

        session.commit()
        session.remove()


# kol_insert()
