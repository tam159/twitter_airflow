from datetime import datetime
import tweepy
from twitter.tweepy_api import api, followers_ids
from dbutils.base import Scoped_session as session

from models.user import UserModel
from models.kol import KolModel

from schemas.user import UserSchema
from schemas.user_stat import UserStatSchema

from ai_modules.age_gender import avatar_resolution
from ai_modules.age_gender import age_gender_pridiction

from crawler.location import location_maching
from crawler.entities_url import entities_url


# New kol exception such as not found, suspended
def new_kol_exception(screen_name, err):
    error_code = eval(err.reason)[0]["code"]
    error = eval(err.reason)[0]["message"]

    # Update kol is not crawled with error_code and error message
    session.query(KolModel).filter(KolModel.screen_name == screen_name).update(
        {
            "crawled_profile": False,
            "error_code": error_code,
            "error": error,
            "priority": None,
            "updated_at": datetime.utcnow(),
        }
    )
    session.commit()

    print(
        "kol_screen_name={} error_code={} error={}".format(
            screen_name, error_code, error
        )
    )
    print(
        "kol_screen_name={} crawled_profile, error_code, error , priority and updated_at were updated".format(
            screen_name
        )
    )


# Update kol exception such as not found, suspended
def existing_kol_exception(id, err):
    error_code = eval(err.reason)[0]["code"]
    error = eval(err.reason)[0]["message"]

    # Update this user in users table
    session.query(UserModel).filter(UserModel.id == id).update(
        {"id_str": error_code, "updated_at": datetime.utcnow()}
    )

    # Update this user in kols table
    session.query(KolModel).filter(KolModel.id == id).update(
        {
            "error_code": error_code,
            "error": error,
            "priority": None,
            "updated_at": datetime.utcnow(),
        }
    )
    session.commit()

    print("user_id={} error_code={} error={}".format(id, error_code, error))


# Update user exception such as not found, suspended
def new_user_exception(id, err):
    error_code = eval(err.reason)[0]["code"]
    error = eval(err.reason)[0]["message"]

    # Update this user in users table
    session.query(UserModel).filter(UserModel.id == id).update(
        {"id_str": error_code, "name": error, "updated_at": datetime.utcnow()}
    )
    session.commit()

    print("user_id={} error_code={} error={}".format(id, error_code, error))


def add_user(user):
    user_schema = UserSchema()
    user_dict = user_schema.dump(user)

    # Update avatar resolution
    user_dict.update(avatar_resolution(user))

    # Add age and gender from AI module
    user_dict.update(age_gender_pridiction(user))

    # Add location
    user_dict.update(location_maching(user))

    # Add entities urls
    user_dict.update(entities_url(user))

    # Update updated_at
    user_dict["updated_at"] = str(datetime.utcnow())

    user_obj = user_schema.load(user_dict, session=session)
    session.add(user_obj)
    session.commit()
    print("user_id={} was crawled and added".format(user.id))


def add_user_stat(user):
    user_stat_schema = UserStatSchema()
    user_stat_dict = user_stat_schema.dump(user)

    user_stat_dict["date_id"] = int(datetime.utcnow().strftime("%Y%m%d"))
    user_stat_dict["time_id"] = int(datetime.utcnow().strftime("%H%M%S"))

    user_stat_obj = user_stat_schema.load(user_stat_dict, session=session)
    session.add(user_stat_obj)
    session.commit()
    print("user_id={} new statistic was added".format(user.id))


def add_followers(user_id):
    new_followers_count = 0
    existing_followers_count = 0
    user = session.query(UserModel).get(user_id)
    try:
        for follower_id in followers_ids(user_id):
            follower_obj = UserModel(id=follower_id)
            # Check if whether the user has a follower, if not then add the user and relationship
            user_has_follower = user.add_follower(follower_obj)
            if user_has_follower:
                existing_followers_count += 1
            else:
                new_followers_count += 1
                existing_followers_count = 0

            if existing_followers_count >= 5:
                print(
                    "user_id={} already had a follower_id={}. Break the rest followers ids checking!".format(
                        user_id, follower_id
                    )
                )
                break

        session.commit()

        print(
            "user_id={} {} new followers ids were added".format(
                user_id, new_followers_count
            )
        )

    except tweepy.error.TweepError as err:
        existing_kol_exception(user_id, err)

    return new_followers_count


def update_user(user):
    full_user_schema = UserSchema()
    user_schema = UserSchema(
        exclude=(
            "interests",
            "user_stats",
            "kol",
            "city",
            "country",
            "updated_at",
            "age",
            "birthyear",
            "gender",
            "ag_ai_version",
            "city_code",
            "country_code",
        )
    )

    # Load a corresponding user from a database
    user_db = session.query(UserModel).get(user.id)
    # Transform the user_db to dictionary format
    user_db_dict = user_schema.dump(user_db)

    # Transform tweepy user to dictionary format
    user_dict = user_schema.dump(user)
    # Update avatar resolution
    user_dict.update(avatar_resolution(user))
    # Add entities urls
    user_dict.update(entities_url(user))

    # Clear None value in both dictionaries
    user_db_dict = {k: v for k, v in user_db_dict.items() if v is not None}
    user_dict = {k: v for k, v in user_dict.items() if v is not None}

    if user_db_dict != user_dict:
        # Check if user changed location
        if user_db.location != user.location:
            # Update location
            user_dict.update(location_maching(user))
            print("user_id={} location updated".format(user.id))

        # Check if user changed avatar
        if user_db.profile_image_url_https != user_dict["profile_image_url_https"]:
            # Call AI API to analyze a new avatar then update
            age_gender_dict = age_gender_pridiction(user)
            user_dict.update(age_gender_dict)
            print("user_id={} avatar updated".format(user.id))

            if "age" in age_gender_dict:
                print("user_id={} age and birthyear were updated".format(user.id))
            if "gender" in age_gender_dict:
                print("user_id={} gender was updated".format(user.id))

        # Transform user_dict to UserModel object
        user_obj = full_user_schema.load(user_dict, session=session)
        # Update updated_at
        user_obj.updated_at = datetime.utcnow()

        # Update the user
        session.add(user_obj)
        session.commit()
        print("user_id={} was updated".format(user.id))

    # If kol is protected and Hiip has not followed and sent follow request, then request
    if (
        user.protected is True
        and user.following is False
        and user.follow_request_sent is False
    ):
        api.create_friendship(user.id)


# user = api.get_user("npt_dc")
# add_user(user)
# update_user(user)
