import time
import tweepy
from twitter.tweepy_api import api


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(1 * 60)


# Cursor
for follower in limit_handled(
    tweepy.Cursor(api.followers, screen_name="realDonaldTrump").items()
):
    # if follower.friends_count < 300:
    print(follower.screen_name)
