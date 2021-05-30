from datetime import datetime
import tweepy
from twitter.tweepy_api import api
from dbutils.base import Scoped_session as session

from models.kol import KolModel

from crawler.user import (
    add_user,
    add_user_stat,
    update_user,
    existing_kol_exception,
    new_kol_exception,
)


# Crawl all Kols profile who have not been crawled
def crawl_new_kols():
    # List of screen_name who have not been crawled
    kols = (
        session.query(KolModel.screen_name)
        .filter(KolModel.crawled_profile == None)
        .order_by(KolModel.priority)
        .all()
    )
    print("List of kols screen_name will be crawled")
    print(kols)

    for kol in kols:
        # Try to crawl kol profile
        try:
            user = api.get_user(kol.screen_name)
        except tweepy.error.TweepError as err:
            new_kol_exception(kol.screen_name, err)
        # Add kol profile and statistic
        else:
            add_user(user)
            add_user_stat(user)

            # Update that kol is crawled and add kol.id in kols table
            session.query(KolModel).filter(
                KolModel.screen_name == kol.screen_name
            ).update(
                {
                    "id": user.id,
                    "crawled_profile": True,
                    "updated_at": datetime.utcnow(),
                }
            )
            session.commit()

            print(
                "kol_screen_name={} id, crawled_profile and updated_at were updated".format(
                    kol.screen_name
                )
            )

            # If user is protected and Hiip has not followed and sent friend request, then request
            if (
                user.protected is True
                and user.following is False
                and user.follow_request_sent is False
            ):
                try:
                    api.create_friendship(user.id)
                except tweepy.error.TweepError as err:
                    error_code = eval(err.reason)[0]["code"]
                    error = eval(err.reason)[0]["message"]
                    print("Friend request failed. {} {}".format(error_code, error))
                else:
                    print(
                        "user_id={}, user_screen_name={} protected={}, friend request was sent".format(
                            user.id, user.screen_name, user.protected
                        )
                    )

    session.commit()
    session.remove()


# Update kols profiles
def update_kols():
    # List of kols ids
    kols = session.query(KolModel.id).filter(KolModel.crawled_profile == True).all()
    print(
        "List of kols will be updated about location, avatar and gender if needed, and statistic"
    )
    print(kols)

    for kol in kols:
        try:
            user = api.get_user(kol.id)
        except tweepy.error.TweepError as err:
            existing_kol_exception(kol.id, err)
        else:
            update_user(user)
            add_user_stat(user)


# crawl_new_kols()
# update_kols()
