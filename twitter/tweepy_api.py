import time
import tweepy
from config import HIIP_SECRETS as secrets

# Twitter credentials for the app
consumer_key = secrets["consumer_key"]
consumer_secret = secrets["consumer_secret"]
access_token = secrets["access_token"]
access_secret = secrets["access_secret"]

# Pass twitter credentials to tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# Initialize tweep api
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(1 * 60)


# def followers_ids(id):
#     return limit_handled(tweepy.Cursor(api.followers_ids, id=id).items())


def followers_ids(id):
    return tweepy.Cursor(api.followers_ids, id=id).items()
