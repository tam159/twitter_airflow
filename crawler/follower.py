from datetime import datetime
import tweepy
from sqlalchemy import and_, or_
from twitter.tweepy_api import api
from dbutils.base import Scoped_session as session

from models.user import UserModel, fans
from models.kol import KolModel

from crawler.user import add_user, add_user_stat, new_user_exception


def crawl_kols_fans(user_id):
    # List of fans ids who have not been crawled
    fans_not_crawled = (
        session.query(UserModel.id)
        .join(fans, UserModel.id == fans.c.follower_id)
        .filter(fans.c.followed_id == user_id)
        .filter(UserModel.name == None)
        .all()
    )
    # Check if there is no new follower
    if len(fans_not_crawled) == 0:
        print("user_id={} no new follower will be crawled".format(user_id))
        # Update fans_profiles_last_crawled of the kol
        session.query(KolModel).filter(KolModel.id == user_id).update(
            {"priority": None, "fans_profiles_last_crawled": datetime.utcnow(),}
        )
        session.commit()
        print("user_id={} fans_profiles_last_crawled were updated".format(user_id))
    # If there are new followers
    else:
        print("user_id={} List of fans ids who have not been crawled".format(user_id))
        print(fans_not_crawled)

        for fan in fans_not_crawled:
            # Try to crawl fan
            try:
                crawled_fan = api.get_user(fan.id)
            except tweepy.error.TweepError as err:
                new_user_exception(fan.id, err)
            else:
                # Add fan profile and statistic
                add_user(crawled_fan)
                add_user_stat(crawled_fan)

        # Recalculate a number of crawled followers
        fans_profiles_count = (
            session.query(UserModel.id)
            .join(fans, UserModel.id == fans.c.follower_id)
            .filter(fans.c.followed_id == user_id)
            .filter(UserModel.screen_name != None)
            .count()
        )

        # Update fans_profiles_count and fans_profiles_last_crawled of the kol
        session.query(KolModel).filter(KolModel.id == user_id).update(
            {
                "priority": None,
                "fans_profiles_count": fans_profiles_count,
                "fans_profiles_last_crawled": datetime.utcnow(),
            }
        )
        session.commit()

        print(
            "user_id={} fans_profiles_count and fans_profiles_last_crawled were updated".format(
                user_id
            )
        )


# Crawl profiles of fans who have not been crawled of kols
def crawl_new_kols_followers():
    # List of new kols ids whose fans have not been crawled and kols do not protect their profile/tweet
    users = (
        session.query(KolModel.id, KolModel.fans_ids_count)
        .join(UserModel)
        .filter(KolModel.fans_ids_count != None, KolModel.fans_profiles_count == None)
        .filter(
            or_(
                UserModel.protected == False,
                and_(UserModel.protected == True, UserModel.following == True),
            )
        )
        .order_by(KolModel.priority)
        .all()
    )
    print(
        "List of new kols ids whose fans have not been crawled and kols do not protect their profile/tweet"
    )
    print(users)

    # For each user
    for user in users:
        # Crawl fans profiles who have not been crawled
        crawl_kols_fans(user.id)

    session.commit()
    session.remove()


# Crawl fans profiles of kols who have more than 10% increase in numbers of followers
# This task runs once per month to update followers profiles of all kols
def crawl_kols_followers():
    # List of new kols ids who do not protect their profile/tweet, whose fans have not been crawled or fans increased
    users = (
        session.query(KolModel.id, KolModel.fans_ids_count)
        .join(UserModel)
        .filter(KolModel.fans_ids_count != None, KolModel.error_code == None,)
        .filter(
            or_(
                UserModel.protected == False,
                and_(UserModel.protected == True, UserModel.following == True),
            )
        )
        .order_by(KolModel.priority)
        .all()
    )
    print(
        "List of new kols ids whose fans have not been crawled or increased and kols do not protect their profile/tweet"
    )
    print(users)

    # For each user
    for user in users:
        # Crawl fans profiles who have not been crawled
        crawl_kols_fans(user.id)

    session.commit()
    session.remove()


# crawl_new_kols_followers()
# crawl_kols_followers()
