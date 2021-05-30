from datetime import datetime
import tweepy
from twitter.tweepy_api import api
from dbutils.base import Scoped_session as session

from models.user import UserModel
from models.kol import KolModel

from crawler.follower import crawl_kols_fans
from crawler.follower_id import add_followers_ids
from crawler.user import existing_kol_exception


# Check if kols accept friend requests, then crawl profiles and fans of the kols
def crawl_protected_kols():
    # List of protected kols ids
    protected_kols = (
        session.query(UserModel.id)
        .join(KolModel)
        .filter(
            UserModel.protected == True,
            UserModel.following == False,
            KolModel.error_code == None,
        )
        .order_by(KolModel.priority)
        .all()
    )

    print("List of protected kols who have not accepted Hiip's friend request")
    print(protected_kols)

    for protected_kol in protected_kols:
        try:
            user = api.get_user(protected_kol.id)
        except tweepy.error.TweepError as err:
            existing_kol_exception(protected_kol.id, err)
        else:
            # If kol is protected and Hiip has not followed and sent follow request, then request
            if (
                user.protected is True
                and user.following is False
                and user.follow_request_sent is False
            ):
                api.create_friendship(user.id)
                print(
                    "user_id={} Hiip have not sent friend request to this user. Sending now!".format(
                        user.id
                    )
                )

            # If kol is not protected or accepted the friend request
            if user.protected is False or user.following is True:
                if user.protected is False:
                    print("user_id={} has de-protected profile".format(user.id))
                if user.following is True:
                    print("user_id={} has accepted the friend request".format(user.id))
                # Update kol profile
                session.query(UserModel).filter(
                    UserModel.id == protected_kol.id
                ).update(
                    {
                        "protected": user.protected,
                        "following": user.following,
                        "updated": datetime.utcnow(),
                    }
                )

                session.commit()
                print(
                    "user_id={} protected, following, updated were updated".format(
                        user.id
                    )
                )

                # Add followers ids
                add_followers_ids(user.id)

                # Crawl fans profile
                crawl_kols_fans(user.id)

            else:
                print("user_id={} has not accepted the friend request".format(user.id))

    session.commit()
    session.remove()


# crawl_protected_kols()
