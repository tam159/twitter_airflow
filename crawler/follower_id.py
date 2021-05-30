from datetime import datetime
from dbutils.base import Scoped_session as session
from sqlalchemy import and_, or_

from models.user import UserModel, fans
from models.kol import KolModel

from crawler.user import add_followers


def add_followers_ids(user_id):
    followers_ids_count = add_followers(user_id)
    # Check if no new follower id was added
    if followers_ids_count == 0:
        # Update fans_ids_last_crawled of the kol
        session.query(KolModel).filter(KolModel.id == user_id).update(
            {"fans_ids_last_crawled": datetime.utcnow()}
        )
        session.commit()
        print("user_id={} fans_ids_last_crawled was updated".format(user_id))
    # If there were new followers ids were added
    else:
        # Update fans_ids_count and fans_ids_last_crawled of the kol
        fans_ids_count = (
            session.query(fans).filter(fans.c.followed_id == user_id).count()
        )
        session.query(KolModel).filter(KolModel.id == user_id).update(
            {
                "fans_ids_count": fans_ids_count,
                "fans_ids_last_crawled": datetime.utcnow(),
            }
        )
        session.commit()
        print(
            "user_id={} fans_ids_count and fans_ids_last_crawled were updated".format(
                user_id
            )
        )


# Crawl followers_ids list of new kols who have no fan
def crawl_new_kols_followers_ids():
    # List of new kols ids who have no fan and do not protect their profile/tweet
    users = (
        session.query(UserModel.id)
        .join(KolModel)
        .filter(KolModel.fans_ids_count == None)
        .filter(
            or_(
                UserModel.protected == False,
                and_(UserModel.protected == True, UserModel.following == True),
            )
        )
        .order_by(KolModel.priority)
        .all()
    )
    print("List of new kols ids who have no fan and do not protect their profile/tweet")
    print(users)

    for user in users:
        # Add a list of followers ids to a user then update the user
        add_followers_ids(user.id)

    session.commit()
    session.remove()


# Crawl followers_ids list of all kols who have more than 10% increase in the number of followers
# This task runs once per month to update followers_ids of all kols
def crawl_kols_followers_ids():
    # List of kols who do not protect their profile/tweet
    users = (
        session.query(UserModel.id)
        .join(KolModel)
        .filter(KolModel.error_code == None)
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
        "List of new kols ids who do not protect their profile/tweet and their followers ids should be updated"
    )
    print(users)

    for user in users:
        # Add a list of followers ids to a user then update the user
        add_followers_ids(user.id)

    session.commit()
    session.remove()


# crawl_new_kols_followers_ids()
# crawl_kols_followers_ids()
