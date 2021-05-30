from pprint import pprint
from twitter.tweepy_api import api

if __name__ == "__main__":
    pass
    # user = api.get_user("sejuta_cinta")
    # pprint(vars(user))
    # kol_schema = KolSchema()
    # kol_stat_schema = KolStatSchema()
    #
    # kol_dict = kol_schema.dump(user)
    # kol_dict.update(age_gender(kol_dict['profile_image_url_https']))
    # kol_obj = kol_schema.load(kol_dict, session=session)
    #
    # kol_stat_dict = kol_stat_schema.dump(user)
    # kol_stat_dict['date_id'] = int(datetime.utcnow().strftime('%Y%m%d'))
    # kol_stat_dict['time_id'] = int(datetime.utcnow().strftime('%H%M%S'))
    # kol_stat_obj = kol_stat_schema.load(kol_stat_dict, session=session)
    #
    # session.add(kol_obj)
    # session.add(kol_stat_obj)
    #
    # session.commit()
    # session.remove()
